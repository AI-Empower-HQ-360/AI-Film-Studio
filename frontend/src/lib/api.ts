// API Client for AI Film Studio Backend
import type { FilmProject } from "@/types/project";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Types for API requests/responses
export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    name: string;
    credits: number;
    subscription_tier: "free" | "pro" | "enterprise";
  };
}

export interface JobStatusResponse {
  job_id: string;
  status: "submitted" | "queued" | "processing" | "completed" | "failed";
  progress: number;
  result?: {
    video_url?: string;
    thumbnail_url?: string;
  };
  error_message?: string;
}

export interface ProjectCreateRequest {
  title: string;
  script: string;
  settings: FilmProject["settings"];
  metadata?: {
    youtubeReference?: string;
  };
}

class APIClient {
  private baseURL: string;
  private token: string | null = null;

  constructor() {
    this.baseURL = API_URL;
    if (typeof window !== "undefined") {
      this.token = localStorage.getItem("auth_token");
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== "undefined") {
      localStorage.setItem("auth_token", token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_token");
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
  ): Promise<T> {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        message: response.statusText,
      }));
      throw new Error(error.message || "API request failed");
    }

    return response.json();
  }

  // Authentication
  async login(email: string, password: string): Promise<AuthResponse> {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    return this.request<AuthResponse>("/api/v1/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });
  }

  async register(
    email: string,
    password: string,
    name: string,
  ): Promise<AuthResponse> {
    return this.request<AuthResponse>("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, name }),
    });
  }

  async getCurrentUser(): Promise<AuthResponse["user"]> {
    return this.request<AuthResponse["user"]>("/api/v1/auth/me");
  }

  // Projects
  async createProject(data: ProjectCreateRequest): Promise<FilmProject> {
    return this.request<FilmProject>("/api/v1/projects", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getProjects(): Promise<FilmProject[]> {
    return this.request<FilmProject[]>("/api/v1/projects");
  }

  async getProject(id: string): Promise<FilmProject> {
    return this.request<FilmProject>(`/api/v1/projects/${id}`);
  }

  async updateProject(
    id: string,
    data: Partial<FilmProject>,
  ): Promise<FilmProject> {
    return this.request<FilmProject>(`/api/v1/projects/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async deleteProject(id: string): Promise<void> {
    return this.request<void>(`/api/v1/projects/${id}`, {
      method: "DELETE",
    });
  }

  // Jobs
  async submitJob(projectId: string): Promise<{ job_id: string }> {
    return this.request<{ job_id: string }>("/api/v1/jobs/submit", {
      method: "POST",
      body: JSON.stringify({ project_id: projectId }),
    });
  }

  async getJobStatus(jobId: string): Promise<JobStatusResponse> {
    return this.request<JobStatusResponse>(`/api/v1/jobs/${jobId}/status`);
  }

  async cancelJob(jobId: string): Promise<void> {
    return this.request<void>(`/api/v1/jobs/${jobId}/cancel`, {
      method: "POST",
    });
  }

  // File uploads
  async uploadFile(file: File, folder: string): Promise<{ url: string }> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("folder", folder);

    const response = await fetch(`${this.baseURL}/api/v1/upload`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Upload failed");
    }

    return response.json();
  }

  // Health check
  async healthCheck(): Promise<{ status: string; version: string }> {
    return this.request<{ status: string; version: string }>("/api/v1/health");
  }

  // Podcast endpoints
  async generatePodcast(data: {
    title: string;
    characters: Array<{
      character_id: string;
      image_url: string;
      voice_id: string;
      name: string;
      role?: string;
    }>;
    dialogue: Array<{
      character_id: string;
      text: string;
      emotion?: string;
      timestamp?: number;
    }>;
    layout?: string;
    background_style?: string;
    add_lower_thirds?: boolean;
    add_background_music?: boolean;
    duration?: number;
  }): Promise<{ job_id: string; status: string }> {
    return this.request<{ job_id: string; status: string }>("/api/v1/podcast/generate", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getPodcastStatus(jobId: string): Promise<{
    job_id: string;
    status: string;
    video_url?: string;
    thumbnail_url?: string;
    duration?: number;
    error_message?: string;
  }> {
    return this.request(`/api/v1/podcast/status/${jobId}`);
  }

  async getPodcastLayouts(): Promise<{
    layouts: Array<{
      layout: string;
      name: string;
      description: string;
      max_characters: number;
    }>;
  }> {
    return this.request("/api/v1/podcast/layouts");
  }

  // Subtitle endpoints
  async generateSubtitles(data: {
    audio_url: string;
    model_name?: string;
    source_language?: string;
    output_format?: string;
    speaker_diarization?: boolean;
    max_line_length?: number;
    languages?: string[];
  }): Promise<{ job_id: string; status: string }> {
    return this.request<{ job_id: string; status: string }>("/api/v1/subtitles/generate", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async translateSubtitles(data: {
    subtitle_url: string;
    target_languages: string[];
    translation_service?: string;
    preserve_timing?: boolean;
  }): Promise<{ job_id: string; status: string }> {
    return this.request<{ job_id: string; status: string }>("/api/v1/subtitles/translate", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async burnSubtitles(data: {
    video_url: string;
    subtitle_url: string;
    font_name?: string;
    font_size?: number;
    font_color?: string;
    background_color?: string;
    position?: string;
  }): Promise<{ job_id: string; status: string }> {
    return this.request<{ job_id: string; status: string }>("/api/v1/subtitles/burn", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getSubtitleStatus(jobId: string): Promise<{
    job_id: string;
    status: string;
    subtitle_urls?: Record<string, string>;
    video_url?: string;
    languages?: string[];
    processing_time?: number;
    error_message?: string;
  }> {
    return this.request(`/api/v1/subtitles/status/${jobId}`);
  }

  async getSupportedLanguages(modelName?: string): Promise<{ languages: string[] }> {
    const params = modelName ? `?model_name=${modelName}` : "";
    return this.request(`/api/v1/subtitles/languages${params}`);
  }

  async getSupportedFormats(): Promise<{ formats: string[] }> {
    return this.request("/api/v1/subtitles/formats");
  }

  async getTranslationServices(): Promise<{ services: any[] }> {
    return this.request("/api/v1/subtitles/translation-services");
  }
}

export const api = new APIClient();
