# AI Film Studio – Copilot Instructions

## Project Overview
AI Film Studio is an AI-powered platform that helps users create films using scripts,
YouTube references, and creative inputs. The system converts ideas into scenes,
videos, narration, and final cinematic output.

## Tech Stack
- Next.js (App Router)
- React
- TypeScript
- Supabase (Authentication, Database, Storage)
- AWS (S3, Lambda, GPU-based APIs)
- AI models for text, image, video, and voice generation

## Repository Structure
- `frontend/src/app` – Application routes and pages
- `frontend/src/components` – UI components and film creation wizards
- `frontend/src/lib` – Utilities, helpers, and shared logic
- `.github/agents` – Specialized GitHub Copilot agents

## Development Guidelines
- Use TypeScript for all new code
- Prefer functional React components
- Keep components modular and reusable
- Avoid breaking existing APIs or workflows
- Follow the existing folder structure

## AI & Copilot Behavior
- Follow repository-wide instructions first
- Use the most relevant agent when responding
- Preserve user creative intent
- Provide production-ready, scalable solutions
- Avoid unnecessary complexity or overengineering
