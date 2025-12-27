# YouTube → Multi-Character AI Video → YouTube Upload (Design Spec)

**Scope:** End-to-end feature delivered in a separate PR (no code in this PR).  
**Goal:** User pastes a YouTube link → transcript/script → select/create characters → generate scenes via external AI video API → stitch MP4 → store in S3 → preview via CloudFront → optional upload to user’s YouTube channel.

## 1) API Design (suggested endpoints)
- `POST /api/v1/youtube/import` — body: `{ youtube_url }`; actions: fetch transcript via YouTube; if absent, enqueue Whisper; returns `script_id`, `job_id`.
- `GET /api/v1/scripts/{script_id}` — fetch normalized script + metadata.
- `POST /api/v1/scripts/{script_id}/characters` — attach character selections `{ character_ids: [], custom_character_ids: [] }`.
- `POST /api/v1/characters` — multipart upload (images) to create custom character; stores metadata + model ref.
- `GET /api/v1/characters` — list pre-made + user-created characters.
- `POST /api/v1/jobs` — start generation for a script + character set → returns `job_id`.
- `GET /api/v1/jobs/{job_id}` — status/progress/errors; includes scene statuses.
- `GET /api/v1/jobs/{job_id}/result` — returns signed S3 URL + CloudFront URL; only when complete.
- `POST /api/v1/jobs/{job_id}/upload-youtube` — triggers Lambda to upload the finalized MP4 to YouTube (requires stored OAuth token).

Notes:
- Auth: JWT; RLS enforced by Supabase for per-user data.  
- Rate limits on import/generation/upload endpoints.

## 2) Worker Pipeline
1. **Transcript acquisition:** Try YouTube transcript; fallback to Whisper API.  
2. **Script normalization:** Clean text; split into scenes (heuristics: timestamps/paragraphs; cap duration per scene).  
3. **Scene breakdown:** Derive scene prompts, camera/style hints, and character bindings.  
4. **Character prep:** If custom, ensure model reference from external API (Replicate/RunDiffusion) is ready.  
5. **Video generation per scene:** Call external AI video API with prompt + character model refs; store scene clips in S3.  
6. **Stitching:** Concatenate clips (ffmpeg), add optional audio bed; output MP4 to S3 (versioned).  
7. **Preview URL:** Generate CloudFront URL (cached) + short-lived signed S3 URL.  
8. **YouTube upload (optional):** Lambda reads MP4 from S3 and calls YouTube Data API v3 using stored OAuth token.  
9. **Progress & errors:** Update `jobs` + `job_events` (optional) with granular status, percent, and error codes.

## 3) Supabase Schema (tables/columns, minimal)
- `users`: id (uuid pk), email, created_at.
- `projects`: id pk, user_id fk, title, status, created_at.
- `scripts`: id pk, project_id fk, youtube_url, raw_transcript, normalized_script, language, created_at.
- `characters`: id pk, user_id fk (nullable for pre-made), name, style, image_url, model_ref, is_premade bool, created_at.
- `assets`: id pk, user_id fk, type (image|video|thumbnail), s3_key or supabase_path, metadata jsonb, created_at.
- `jobs`: id pk, project_id fk, type (import|generation|upload), status (queued|running|failed|succeeded), progress int, error_code (varchar(50)), error_message (text), result_s3_key, result_cf_url, created_at, updated_at.
- `job_scenes`: id pk, job_id fk, scene_index, status, progress, s3_key, error_code (varchar(50)), error_message (text), prompt jsonb.
- `oauth_tokens`: id pk, user_id fk, provider (google), scope, access_token (encrypted), refresh_token (encrypted), expires_at, revoked_at, created_at.

Indexes: by user_id, status, created_at. RLS: per-user on user-owned rows; premade characters readable by all.

## 4) OAuth (YouTube upload)
- Frontend initiates Google OAuth with `youtube.upload` scope.  
- Backend receives code → exchanges for tokens → encrypts and stores in `oauth_tokens`.  
- Refresh tokens handled server-side before upload; short-lived access tokens cached in memory/Redis.  
- Upload flow: API `POST /jobs/{id}/upload-youtube` enqueues Lambda task with S3 key + token ref; Lambda performs upload and updates job status.

## 5) External AI Integrations
- Transcript: YouTube transcript API; fallback Whisper API (batch, paid).  
- Character model: Replicate / RunDiffusion API; input = user images; output = model_ref or LoRA reference.  
- Video generation: Replicate / RunDiffusion / Pika — input prompt + model_ref + character image; output MP4 per scene.  
- Config via env/Secrets Manager; retry with backoff; capture provider request/response IDs for support.

## 6) Frontend Flows (Next.js)
- Page: “Create from YouTube” with input for link, “Import” action.  
- Transcript preview + inline script editor (optional trims).  
- Character selection panel (pre-made + custom); custom upload dropzone.  
- “Generate Video” button → shows job progress (polling `/jobs/{id}`).  
- Preview player with CloudFront URL; download link (signed S3).  
- “Upload to YouTube” button (requires connected account); handles OAuth connect if missing; shows upload status.

## 7) Error Handling & Logging
- Structured logs with request/job IDs; capture provider response codes.  
- Error taxonomy: `TRANSCRIPT_MISSING`, `AI_PROVIDER_FAILURE`, `UPLOAD_FAILED`, `OAUTH_EXPIRED`, `SCENE_TIMEOUT`, etc.  
- Jobs record both fatal and per-scene errors; retries for transient provider/FFmpeg/S3 errors.  
- User-facing messages sanitized; internal details in logs/CloudWatch.

Example error codes (extend as needed):
| Code | Meaning | Suggested user action |
| --- | --- | --- |
| TRANSCRIPT_MISSING | Transcript unavailable from YouTube and Whisper failed | Retry with clearer audio or different link |
| AI_PROVIDER_FAILURE | External AI API returned error/timeout | Retry; if persistent, switch provider/region |
| SCENE_TIMEOUT | Scene generation exceeded time budget | Retry; reduce scene length/complexity |
| OAUTH_EXPIRED | Stored OAuth token invalid/expired | Re-connect Google/YouTube account |
| UPLOAD_FAILED | YouTube upload failed (quota/auth/network) | Retry; verify OAuth scope/quota |
| STITCH_FAILED | FFmpeg stitching failed | Retry; verify scene assets intact |

## 8) Security & Production Readiness
- Supabase RLS for user-owned tables; premade characters read-only public.  
- Encrypt tokens at rest; do not log secrets; scoped least-privilege IAM for S3/Lambda.  
- S3 signed URLs for downloads; CloudFront caching for previews (private behavior).  
- Rate limiting on import/generation/upload endpoints; input validation on URLs/files.  
- Observability: metrics for job success/latency; alerts on failure rates and provider errors.

## 9) Phased Implementation Plan (separate PRs)
1) Schema & API contracts (no external calls) + stubs/tests.  
2) Transcript import + Whisper fallback; script normalization; job status infra.  
3) Character CRUD/upload + external character model creation.  
4) Scene breakdown + external video generation + stitching to S3 + preview URLs.  
5) YouTube OAuth + upload Lambda + end-to-end happy path.  
6) Frontend flows (import → edit → select characters → generate → preview → upload) + E2E smoke.  
7) Hardening: retries, metrics, alerts, rate limits, RLS verification, load tests.
