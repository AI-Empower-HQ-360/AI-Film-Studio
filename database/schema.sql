-- AI Film Studio Database Schema
-- PostgreSQL 15+
-- Version: 1.0
-- Last Updated: 2025-12-31

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- USERS TABLE
-- ============================================================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    tier VARCHAR(50) NOT NULL DEFAULT 'free' CHECK (tier IN ('free', 'pro', 'enterprise', 'admin')),
    credits INTEGER NOT NULL DEFAULT 3,
    credit_reset_date TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP + INTERVAL '30 days'),
    
    -- Profile information
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    avatar_url TEXT,
    locale VARCHAR(10) DEFAULT 'en',
    
    -- Account status
    is_active BOOLEAN NOT NULL DEFAULT true,
    email_verified BOOLEAN NOT NULL DEFAULT false,
    email_verified_at TIMESTAMP,
    
    -- OAuth information
    oauth_provider VARCHAR(50),
    oauth_id VARCHAR(255),
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Indexes for users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_tier ON users(tier);
CREATE INDEX idx_users_oauth ON users(oauth_provider, oauth_id);
CREATE INDEX idx_users_deleted_at ON users(deleted_at) WHERE deleted_at IS NULL;

-- ============================================================================
-- PROJECTS TABLE
-- ============================================================================
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Project details
    title VARCHAR(255) NOT NULL,
    script TEXT NOT NULL,
    description TEXT,
    
    -- Status and configuration
    status VARCHAR(50) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'queued', 'processing', 'completed', 'failed', 'cancelled')),
    style VARCHAR(50) DEFAULT 'cinematic' CHECK (style IN ('cinematic', 'anime', 'documentary', 'cartoon', 'photorealistic')),
    target_duration INTEGER DEFAULT 60, -- in seconds
    actual_duration INTEGER, -- in seconds
    
    -- Output URLs
    thumbnail_url TEXT,
    output_url_720p TEXT,
    output_url_1080p TEXT,
    subtitles_url TEXT,
    
    -- Settings
    settings JSONB DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Indexes for projects table
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);
CREATE INDEX idx_projects_deleted_at ON projects(deleted_at) WHERE deleted_at IS NULL;

-- ============================================================================
-- JOBS TABLE
-- ============================================================================
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Job details
    type VARCHAR(50) NOT NULL CHECK (type IN ('script_analysis', 'image_generation', 'voice_synthesis', 'video_composition', 'subtitle_generation', 'thumbnail_generation', 'full_generation')),
    status VARCHAR(50) NOT NULL DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'cancelled')),
    
    -- Progress tracking
    progress INTEGER NOT NULL DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    current_step VARCHAR(255),
    
    -- Job configuration and results
    parameters JSONB DEFAULT '{}',
    result JSONB,
    output_url TEXT,
    error_message TEXT,
    error_details JSONB,
    
    -- Priority and timing
    priority INTEGER NOT NULL DEFAULT 1 CHECK (priority BETWEEN 1 AND 3), -- 1=low, 2=normal, 3=high
    retry_count INTEGER NOT NULL DEFAULT 0,
    max_retries INTEGER NOT NULL DEFAULT 3,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    failed_at TIMESTAMP
);

-- Indexes for jobs table
CREATE INDEX idx_jobs_project_id ON jobs(project_id);
CREATE INDEX idx_jobs_user_id ON jobs(user_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_type ON jobs(type);
CREATE INDEX idx_jobs_priority ON jobs(priority DESC);
CREATE INDEX idx_jobs_created_at ON jobs(created_at DESC);

-- ============================================================================
-- CREDIT TRANSACTIONS TABLE
-- ============================================================================
CREATE TABLE credit_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Transaction details
    type VARCHAR(50) NOT NULL CHECK (type IN ('deduction', 'purchase', 'grant', 'refund', 'reset')),
    amount INTEGER NOT NULL, -- positive for addition, negative for deduction
    balance_before INTEGER NOT NULL,
    balance_after INTEGER NOT NULL,
    
    -- Transaction metadata
    description TEXT,
    metadata JSONB DEFAULT '{}',
    
    -- Related entities
    project_id UUID REFERENCES projects(id),
    job_id UUID REFERENCES jobs(id),
    
    -- Payment information (for purchases)
    payment_id VARCHAR(255),
    payment_provider VARCHAR(50),
    payment_amount DECIMAL(10, 2),
    payment_currency VARCHAR(3),
    
    -- Timestamp
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for credit_transactions table
CREATE INDEX idx_credit_transactions_user_id ON credit_transactions(user_id);
CREATE INDEX idx_credit_transactions_type ON credit_transactions(type);
CREATE INDEX idx_credit_transactions_created_at ON credit_transactions(created_at DESC);

-- ============================================================================
-- YOUTUBE INTEGRATIONS TABLE
-- ============================================================================
CREATE TABLE youtube_integrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- YouTube account details
    channel_id VARCHAR(255) NOT NULL,
    channel_name VARCHAR(255),
    channel_thumbnail_url TEXT,
    
    -- OAuth tokens
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    token_expires_at TIMESTAMP NOT NULL,
    scope TEXT,
    
    -- Status
    is_active BOOLEAN NOT NULL DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP
);

-- Indexes for youtube_integrations table
CREATE INDEX idx_youtube_integrations_user_id ON youtube_integrations(user_id);
CREATE INDEX idx_youtube_integrations_channel_id ON youtube_integrations(channel_id);
CREATE UNIQUE INDEX idx_youtube_integrations_unique ON youtube_integrations(user_id, channel_id);

-- ============================================================================
-- YOUTUBE UPLOADS TABLE
-- ============================================================================
CREATE TABLE youtube_uploads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    youtube_integration_id UUID NOT NULL REFERENCES youtube_integrations(id) ON DELETE CASCADE,
    
    -- YouTube video details
    video_id VARCHAR(255) NOT NULL,
    video_title VARCHAR(255) NOT NULL,
    video_description TEXT,
    video_url TEXT NOT NULL,
    
    -- Upload status
    status VARCHAR(50) NOT NULL DEFAULT 'uploading' CHECK (status IN ('uploading', 'processing', 'live', 'failed', 'deleted')),
    upload_progress INTEGER DEFAULT 0 CHECK (upload_progress >= 0 AND upload_progress <= 100),
    
    -- Video metadata
    privacy_status VARCHAR(50) DEFAULT 'private' CHECK (privacy_status IN ('public', 'private', 'unlisted')),
    category_id VARCHAR(50),
    tags TEXT[],
    playlist_id VARCHAR(255),
    
    -- Statistics
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    
    -- Error information
    error_message TEXT,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Indexes for youtube_uploads table
CREATE INDEX idx_youtube_uploads_project_id ON youtube_uploads(project_id);
CREATE INDEX idx_youtube_uploads_user_id ON youtube_uploads(user_id);
CREATE INDEX idx_youtube_uploads_video_id ON youtube_uploads(video_id);
CREATE INDEX idx_youtube_uploads_status ON youtube_uploads(status);
CREATE INDEX idx_youtube_uploads_created_at ON youtube_uploads(created_at DESC);

-- ============================================================================
-- FUNCTIONS AND TRIGGERS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_youtube_integrations_updated_at BEFORE UPDATE ON youtube_integrations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_youtube_uploads_updated_at BEFORE UPDATE ON youtube_uploads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE users IS 'User accounts and authentication information';
COMMENT ON TABLE projects IS 'Film projects created by users';
COMMENT ON TABLE jobs IS 'AI processing jobs for film generation';
COMMENT ON TABLE credit_transactions IS 'Credit usage and purchase history';
COMMENT ON TABLE youtube_integrations IS 'YouTube account connections';
COMMENT ON TABLE youtube_uploads IS 'Videos uploaded to YouTube';
