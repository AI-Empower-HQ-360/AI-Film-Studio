# Amplify Hosting + Supabase Backend Setup (Scaffolding Plan)

**Scope:** End-to-end scaffolding (no code deploys) for AI Film Studio: Amplify-hosted Next.js frontend, Supabase auth/DB/storage, AWS Lambda/S3/CloudFront helpers, and external AI/YouTube integrations. Use this as the checklist for the dedicated implementation PR.

## 1) Amplify Hosting (Next.js)
- **amplify.yml** (build & deploy):
  ```yaml
  version: 1
  applications:
    - appRoot: .
      frontend:
        phases:
          preBuild:
            commands:
              - npm ci
          build:
            commands:
              - npm run build
        artifacts:
          baseDirectory: .next
          files:
            - '**/*'
        cache:
          paths:
            - node_modules/**/*
            - .next/cache/**/*
  ```
- **GitHub connection:** Connect repo in Amplify console; select `copilot/check-files-for-production` or main branch; enable auto-builds.
- **Env vars (Amplify):**  
  - `NEXT_PUBLIC_SUPABASE_URL`  
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`  
  - `SUPABASE_SERVICE_ROLE_KEY` (backend-only usages; keep in Amplify build secrets)  
  - `SUPABASE_STORAGE_BUCKET_USER_IMAGES`, `SUPABASE_STORAGE_BUCKET_CHARACTER_IMAGES`, `SUPABASE_STORAGE_BUCKET_METADATA`  
  - `S3_TEMP_BUCKET`, `CLOUDFRONT_DIST_ID`, `CLOUDFRONT_DOMAIN`  
  - `YOUTUBE_OAUTH_CLIENT_ID`, `YOUTUBE_OAUTH_CLIENT_SECRET`, `YOUTUBE_OAUTH_REDIRECT_URI`  
  - `AI_REPLICATE_API_TOKEN`, `AI_PIKA_API_TOKEN`, `AI_RUN_DIFFUSION_TOKEN`, `WHISPER_API_KEY`
- **Routing structure (Next.js):**
  - `/` landing
  - `/auth/login`, `/auth/signup`
  - `/dashboard` (projects list)
  - `/projects/[id]` (transcript preview, script editor, character selection, job progress, video preview, upload-to-YouTube)
  - `/characters` (library + custom uploads)
  - `/settings/connections` (YouTube OAuth connect)

## 2) Supabase schema (SQL skeleton)
```sql
-- users via Supabase auth (id uuid)

create table projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  title text,
  status text,
  created_at timestamptz default now()
);

create table scripts (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references projects(id),
  youtube_url text,
  raw_transcript text,
  normalized_script text,
  language text,
  created_at timestamptz default now()
);

create table characters (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  name text,
  style text,
  image_url text,
  model_ref text,
  is_premade boolean default false,
  created_at timestamptz default now()
);

create table assets (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  type text, -- image|video|thumbnail
  storage_path text,
  metadata jsonb,
  created_at timestamptz default now()
);

create table jobs (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references projects(id),
  type text, -- import|generation|upload
  status text, -- queued|running|failed|succeeded
  progress int,
  error_code varchar(50),
  error_message text,
  result_s3_key text,
  result_cf_url text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table job_scenes (
  id uuid primary key default gen_random_uuid(),
  job_id uuid references jobs(id),
  scene_index int,
  status text,
  progress int,
  s3_key text,
  error_code varchar(50),
  error_message text,
  prompt jsonb
);

create table oauth_tokens (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  provider text, -- google
  scope text,
  access_token text,
  refresh_token text,
  expires_at timestamptz,
  revoked_at timestamptz,
  created_at timestamptz default now()
);
```

### RLS (examples, apply per table)
```sql
alter table projects enable row level security;
create policy "user owns project" on projects
  for all using (auth.uid() = user_id);

alter table characters enable row level security;
create policy "user owns character" on characters
  for select using (is_premade OR auth.uid() = user_id)
  with check (auth.uid() = user_id OR is_premade);

alter table assets enable row level security;
create policy "user owns asset" on assets
  for all using (auth.uid() = user_id);
```

### Storage buckets
- `user-images`, `character-images`, `metadata` with bucket policies limiting to `auth.uid()` paths.

## 3) AWS helpers (Lambda/S3/CloudFront) — stubs
- Functions (placeholder handlers; infra to be provisioned separately):
  - `extract_youtube_transcript`
  - `whisper_fallback_transcription`
  - `generate_script_from_transcript`
  - `generate_ai_video` (calls external AI providers)
  - `stitch_scenes_into_video`
  - `upload_to_youtube` (YouTube Data API v3)
  - `upload_to_s3` (signed URL helper)
- S3: temp bucket for videos; lifecycle rule delete after 1 day.
- CloudFront: distribution over temp bucket for previews; signed URLs for private access.

## 4) External integrations (helpers to scaffold)
- YouTube Transcript API client + fallback Whisper call.
- AI providers (Replicate / RunDiffusion / Pika): thin clients with retries/backoff, returning MP4 clip URLs.
- YouTube Data API v3 uploader using stored OAuth tokens; refresh when expired.

## 5) Frontend wiring (Next.js scaffold guidance)
- Supabase client singleton (service role on server, anon on client).
- Auth guard HOCs / middleware.
- API route stubs for: import link, start job, poll job, list characters, create character (upload + model_ref), request upload-to-YouTube.
- Components: YouTube input, transcript viewer/editor, character picker, image uploader, job progress, video preview/player, upload-to-YouTube CTA.

## 6) Env templates
- `.env.local.example` (frontend):
  ```
  NEXT_PUBLIC_SUPABASE_URL=
  NEXT_PUBLIC_SUPABASE_ANON_KEY=
  NEXT_PUBLIC_CLOUDFRONT_DOMAIN=
  NEXT_PUBLIC_S3_TEMP_BUCKET=
  NEXT_PUBLIC_YOUTUBE_CLIENT_ID=
  ```
- `.env.backend.example` (server/Lambda/Edge):
  ```
  SUPABASE_URL=
  SUPABASE_SERVICE_ROLE_KEY=
  S3_TEMP_BUCKET=
  CLOUDFRONT_DIST_ID=
  CLOUDFRONT_DOMAIN=
  AI_REPLICATE_API_TOKEN=
  AI_PIKA_API_TOKEN=
  AI_RUN_DIFFUSION_TOKEN=
  WHISPER_API_KEY=
  YOUTUBE_OAUTH_CLIENT_ID=
  YOUTUBE_OAUTH_CLIENT_SECRET=
  YOUTUBE_OAUTH_REDIRECT_URI=
  ```

## 7) Workflow overview (to implement)
1) Frontend posts YouTube URL → API stores script record, creates `jobs` row (import).  
2) Lambda extracts transcript or uses Whisper; updates `scripts` and job status.  
3) User edits script; selects characters (pre-made/custom). Custom upload → Supabase Storage → character model creation via AI provider → store `model_ref`.  
4) Generation job enqueued: per-scene calls to AI video API → clips to S3 → stitch → final MP4 to S3; job_scenes and jobs updated.  
5) Preview via CloudFront signed URL; optional download via signed S3 URL.  
6) Upload to YouTube: Lambda uses stored OAuth token (refresh if needed) → YouTube Data API v3; updates job status.

## 8) Security & prod notes
- Use Supabase RLS everywhere; encrypt tokens; never log secrets.  
- IAM least-privilege for Lambdas to only needed S3/CloudFront actions.  
- Rate-limit import/generation/upload endpoints.  
- Observability: per-job metrics, error codes, and traces.  
- Lifecycle policies on temp S3.  
- CSP/CORS tightened to Amplify domain and CloudFront.

## 9) Next steps (PR plan)
- Add concrete infra definitions (Amplify app settings, Supabase migrations, IaC for Lambdas/S3/CloudFront).  
- Implement API route stubs and client hooks.  
- Add CI to lint/test/build Next.js and run Supabase migration checks.  
- Wire E2E smoke for import → generate → preview → upload (happy path).
