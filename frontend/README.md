# 🎬 AI Film Studio - Frontend

A modern Next.js 14 frontend application with Supabase authentication, built with TypeScript and Tailwind CSS.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Supabase Setup](#supabase-setup)
- [Running the Application](#running-the-application)
- [Building for Production](#building-for-production)
- [Project Structure](#project-structure)
- [Features](#features)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This is the frontend application for AI Film Studio, providing a user interface for creating AI-generated films from scripts. Built with modern web technologies:

- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Supabase** for authentication and database
- **Tailwind CSS** for styling
- **Server-Side Rendering** for optimal performance

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** >= 18.x
- **npm** >= 9.x (comes with Node.js)
- A **Supabase account** (free tier available at [supabase.com](https://supabase.com))

---

## 📦 Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

   This will install all required packages including:
   - Next.js 14
   - React 18
   - Supabase client libraries
   - Tailwind CSS
   - TypeScript

---

## 🔐 Environment Configuration

1. **Copy the environment example file:**
   ```bash
   cp .env.local.example .env.local
   ```

2. **The `.env.local` file is pre-configured with Supabase credentials:**
   ```env
   # Supabase Configuration
   NEXT_PUBLIC_SUPABASE_URL=https://spfefoaeyowaojgqtxxo.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_oDObTtUno0j_-7Pz_gAaaw_KHe4vF-q
   SUPABASE_SERVICE_ROLE_KEY=sb_secret_Gnf6P-g42GzzfckiFu9gkw_E4lO8Oem

   # AWS CloudFront (for video delivery) - Optional
   NEXT_PUBLIC_CLOUDFRONT_DOMAIN=

   # AWS S3 (for temporary uploads) - Optional
   NEXT_PUBLIC_S3_TEMP_BUCKET=

   # YouTube Integration (for video uploads) - Optional
   NEXT_PUBLIC_YOUTUBE_CLIENT_ID=
   ```

   ✅ **All Supabase keys are already filled in** - no need to find them!

---

## 🗄️ Supabase Setup

### Step 1: Access Supabase Dashboard

1. Go to [https://supabase.com](https://supabase.com)
2. Sign in or create a free account
3. Navigate to your project: `spfefoaeyowaojgqtxxo`

### Step 2: Configure Email Authentication

1. In Supabase Dashboard, go to **Authentication** → **Providers**
2. Ensure **Email** provider is enabled
3. Configure the following settings:
   - Enable Email provider
   - Disable "Confirm email" if you want instant access (or keep enabled for production)
   - Set "Site URL" to: `http://localhost:3000` (for local development)
   - Add redirect URLs:
     - `http://localhost:3000/auth/callback`
     - `http://localhost:3000/dashboard`

### Step 3: Configure Email Templates (Optional)

1. Go to **Authentication** → **Email Templates**
2. Customize the confirmation email template if needed
3. Update the redirect URL in templates to match your domain

### Step 4: Set Up Database Tables

Run this SQL in the Supabase **SQL Editor** to create required tables and security policies:

```sql
-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  email TEXT,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Create policies for profiles table
CREATE POLICY "Users can view own profile" 
  ON profiles FOR SELECT 
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" 
  ON profiles FOR UPDATE 
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" 
  ON profiles FOR INSERT 
  WITH CHECK (auth.uid() = id);

-- Create function to automatically create profile on user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name)
  VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'full_name');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger to call function on new user creation
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();
```

**What this does:**
- Creates a `profiles` table linked to Supabase Auth users
- Enables Row Level Security (RLS) so users can only see their own data
- Automatically creates a profile when a user signs up
- Sets up proper access policies

### Step 5: Verify URL Configuration

1. Go to **Settings** → **API**
2. Verify your Project URL matches: `https://spfefoaeyowaojgqtxxo.supabase.co`
3. Verify your anon/public key matches the one in `.env.local`

---

## 🚀 Running the Application

### Development Mode

Start the development server:

```bash
npm run dev
```

The application will be available at: **http://localhost:3000**

### What you'll see:

1. **Landing Page** (`/`) - Welcome page with feature overview
2. **Sign Up** (`/signup`) - Create a new account
3. **Login** (`/login`) - Sign in to existing account
4. **Dashboard** (`/dashboard`) - Protected page showing user info (requires authentication)

---

## 🏗️ Building for Production

### Build the application:

```bash
npm run build
```

### Start the production server:

```bash
npm start
```

The production build optimizes the application for performance:
- Minifies JavaScript and CSS
- Optimizes images
- Pre-renders static pages
- Enables server-side rendering

---

## 📁 Project Structure

```
frontend/
├── app/                          # Next.js App Router
│   ├── layout.tsx                # Root layout with metadata
│   ├── page.tsx                  # Landing page
│   ├── globals.css               # Global styles with Tailwind
│   ├── login/
│   │   └── page.tsx              # Login page
│   ├── signup/
│   │   └── page.tsx              # Sign up page
│   ├── dashboard/
│   │   └── page.tsx              # Protected dashboard
│   └── auth/
│       └── callback/
│           └── route.ts          # OAuth callback handler
│
├── components/                   # React components
│   └── auth/
│       ├── SignInForm.tsx        # Login form component
│       ├── SignUpForm.tsx        # Registration form component
│       └── SignOutButton.tsx     # Sign out button component
│
├── lib/                          # Utility libraries
│   └── supabase/
│       ├── client.ts             # Browser Supabase client
│       ├── server.ts             # Server Supabase client
│       └── middleware.ts         # Auth middleware utilities
│
├── types/                        # TypeScript type definitions
│   └── supabase.ts               # Supabase database types
│
├── public/                       # Static assets
│   └── .gitkeep
│
├── middleware.ts                 # Next.js middleware (auth)
├── .env.local.example            # Environment variables template
├── .gitignore                    # Git ignore rules
├── next.config.js                # Next.js configuration
├── package.json                  # Dependencies and scripts
├── postcss.config.js             # PostCSS configuration
├── tailwind.config.ts            # Tailwind CSS configuration
├── tsconfig.json                 # TypeScript configuration
└── README.md                     # This file
```

---

## ✨ Features

### Authentication
- ✅ Email/password authentication via Supabase
- ✅ Email confirmation workflow
- ✅ Protected routes with middleware
- ✅ Automatic session management
- ✅ Secure cookie-based auth

### UI/UX
- ✅ Modern, responsive design with Tailwind CSS
- ✅ Gradient backgrounds and smooth transitions
- ✅ Form validation and error handling
- ✅ Loading states for async operations
- ✅ Success/error messages

### Security
- ✅ Row Level Security (RLS) in Supabase
- ✅ HTTP-only cookies for session management
- ✅ Server-side authentication checks
- ✅ CSRF protection via Supabase

### Developer Experience
- ✅ Full TypeScript support
- ✅ Hot module replacement in development
- ✅ ESLint configuration
- ✅ Automatic type generation from Supabase

---

## 🔧 Troubleshooting

### Issue: "Cannot find module '@supabase/ssr'"

**Solution:** Ensure all dependencies are installed:
```bash
npm install
```

### Issue: "Environment variables not defined"

**Solution:** 
1. Verify `.env.local` exists in the `frontend/` directory
2. Ensure it contains all required variables from `.env.local.example`
3. Restart the development server after adding/changing variables

### Issue: "Invalid login credentials"

**Solution:**
1. Verify the email and password are correct
2. Check if email confirmation is required in Supabase settings
3. If using a new account, check your email for the confirmation link

### Issue: "Failed to fetch" or connection errors

**Solution:**
1. Verify Supabase credentials in `.env.local`
2. Check your Supabase project is active (not paused)
3. Ensure you have internet connectivity
4. Verify the Supabase URL is correct: `https://spfefoaeyowaojgqtxxo.supabase.co`

### Issue: Email confirmation not working

**Solution:**
1. Check Supabase Dashboard → Authentication → Providers
2. Verify "Confirm email" setting matches your needs
3. Check spam/junk folder for confirmation emails
4. Ensure redirect URLs are configured correctly in Supabase

### Issue: Dashboard redirects to login

**Solution:**
1. Sign in first at `/login`
2. Clear browser cookies and try again
3. Check browser console for authentication errors
4. Verify middleware is working correctly

### Issue: Port 3000 already in use

**Solution:**
```bash
# Kill the process using port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
npm run dev -- -p 3001
```

### Issue: Build fails with TypeScript errors

**Solution:**
```bash
# Clean Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Try building again
npm run build
```

---

## 🧪 Testing the Application

### Manual Testing Checklist

1. **Landing Page**
   - [ ] Visit http://localhost:3000
   - [ ] Verify page loads with AI Film Studio branding
   - [ ] Click "Get Started" → should go to `/signup`
   - [ ] Click "Sign In" → should go to `/login`

2. **Sign Up Flow**
   - [ ] Visit `/signup`
   - [ ] Enter email and password (min 6 characters)
   - [ ] Submit form
   - [ ] Verify success message appears
   - [ ] Check email inbox for confirmation (if enabled)

3. **Login Flow**
   - [ ] Visit `/login`
   - [ ] Enter registered email and password
   - [ ] Submit form
   - [ ] Should redirect to `/dashboard`

4. **Dashboard**
   - [ ] Verify user email is displayed
   - [ ] Verify user ID is shown
   - [ ] Check email confirmation status
   - [ ] Click "Sign Out" → should redirect to `/login`

5. **Protected Route**
   - [ ] Sign out
   - [ ] Try accessing `/dashboard` directly
   - [ ] Should redirect to `/login`

---

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)

---

## 🤝 Support

If you encounter issues:

1. Check this README's [Troubleshooting](#troubleshooting) section
2. Review Supabase Dashboard logs
3. Check browser console for errors
4. Review Next.js server logs in terminal

---

## 📝 License

This project is part of the AI Film Studio platform. See the main repository LICENSE file for details.

---

**Built with ❤️ using Next.js, Supabase, and Tailwind CSS**
