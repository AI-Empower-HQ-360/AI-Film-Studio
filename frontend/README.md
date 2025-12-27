# AI Film Studio - Frontend

A modern Next.js 14 frontend application with complete Supabase authentication integration.

## 🎯 Features

- ✅ **Next.js 14 App Router** - Modern React framework with server components
- ✅ **Supabase Authentication** - Complete auth flow (sign up, sign in, sign out)
- ✅ **TypeScript** - Type-safe development
- ✅ **TailwindCSS** - Beautiful, responsive UI
- ✅ **Protected Routes** - Middleware-based authentication
- ✅ **Server Components** - Optimized performance
- ✅ **Email Confirmation** - Secure user verification

## 📋 Prerequisites

- Node.js >= 18.x
- npm or yarn
- Supabase account

## 🚀 Getting Started

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Set Up Environment Variables

Create a `.env.local` file in the `frontend` directory:

```bash
cp .env.local.example .env.local
```

The file should contain:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

**Note:** Replace these placeholder values with your actual Supabase project credentials from your [Supabase Dashboard](https://app.supabase.com).

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Build for Production

```bash
npm run build
npm start
```

## 🗄️ Supabase Setup

### Configure Supabase Project

1. Go to your [Supabase Dashboard](https://app.supabase.com)
2. Select your project or create a new one
3. Navigate to **Authentication** → **URL Configuration**
4. Add the following redirect URLs:
   - `http://localhost:3000/auth/callback` (for development)
   - `https://yourdomain.com/auth/callback` (for production)

### Create Database Tables

Run the following SQL in the Supabase SQL Editor:

#### 1. Create Profiles Table

```sql
-- Create profiles table
CREATE TABLE profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  email TEXT,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
```

#### 2. Create RLS Policies

```sql
-- Users can view their own profile
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- Users can insert their own profile
CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);
```

#### 3. Create Trigger for Auto-Profile Creation

```sql
-- Function to handle new user creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name)
  VALUES (
    NEW.id,
    NEW.email,
    NEW.raw_user_meta_data->>'full_name'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to automatically create profile on user signup
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();
```

### Configure Email Templates

1. Go to **Authentication** → **Email Templates**
2. Customize the confirmation email template
3. Ensure email confirmation is enabled in **Authentication** → **Providers** → **Email**

## 📁 Project Structure

```
frontend/
├── app/                        # Next.js 14 App Router
│   ├── auth/                   # Auth routes
│   │   └── callback/           # OAuth callback handler
│   │       └── route.ts
│   ├── login/                  # Login page
│   │   └── page.tsx
│   ├── signup/                 # Signup page
│   │   └── page.tsx
│   ├── dashboard/              # Protected dashboard
│   │   └── page.tsx
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Landing page
│   └── globals.css             # Global styles
├── components/                 # React components
│   └── auth/                   # Authentication components
│       ├── SignInForm.tsx      # Login form
│       ├── SignUpForm.tsx      # Registration form
│       └── SignOutButton.tsx   # Logout button
├── lib/                        # Libraries and utilities
│   └── supabase/               # Supabase clients
│       ├── client.ts           # Browser client
│       ├── server.ts           # Server-side client
│       └── middleware.ts       # Session management
├── types/                      # TypeScript types
│   └── supabase.ts             # Database types
├── middleware.ts               # Next.js middleware
├── .env.local.example          # Environment template
├── .gitignore                  # Git ignore rules
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── next.config.js              # Next.js config
├── tailwind.config.ts          # Tailwind config
├── postcss.config.js           # PostCSS config
└── README.md                   # This file
```

## 🔐 Authentication Flow

### Sign Up Flow

1. User fills out the registration form
2. Supabase creates the user account
3. Confirmation email is sent
4. User clicks the confirmation link
5. User is redirected to dashboard

### Sign In Flow

1. User enters email and password
2. Supabase validates credentials
3. Session is created
4. User is redirected to dashboard

### Protected Routes

The middleware automatically:
- Manages session cookies
- Refreshes expired sessions
- Protects authenticated routes

## 🎨 Styling

The application uses **TailwindCSS** with a custom color scheme:

- **Primary**: Blue tones (`primary-50` to `primary-900`)
- **Success**: Green tones
- **Error**: Red tones
- **Background**: Gray-50

All components are fully responsive and work on mobile and desktop.

## 🧪 Testing Authentication

### Test Sign Up

1. Navigate to [http://localhost:3000/signup](http://localhost:3000/signup)
2. Enter email and password (min 6 characters)
3. Check your email for confirmation
4. Click the confirmation link

### Test Sign In

1. Navigate to [http://localhost:3000/login](http://localhost:3000/login)
2. Enter your credentials
3. You should be redirected to `/dashboard`

### Test Protected Route

1. Try accessing [http://localhost:3000/dashboard](http://localhost:3000/dashboard) without being logged in
2. You should be redirected to login

## 🔧 Common Issues

### "Invalid login credentials"

- Ensure you've confirmed your email
- Check that your password is correct
- Verify environment variables are set correctly

### "redirect_to not allowed"

- Add your callback URL to Supabase dashboard
- Check **Authentication** → **URL Configuration**

### Session not persisting

- Clear browser cookies
- Restart the development server
- Check middleware configuration

### TypeScript errors

```bash
npm run build
```

This will show any type errors that need to be fixed.

## 📚 Key Technologies

- **Next.js 14**: React framework with App Router
- **@supabase/ssr**: Server-side rendering support
- **@supabase/supabase-js**: Supabase JavaScript client
- **TypeScript**: Type safety
- **TailwindCSS**: Utility-first CSS framework

## 🔗 Useful Links

- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Auth Helpers for Next.js](https://supabase.com/docs/guides/auth/auth-helpers/nextjs)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

## 🚀 Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import your repository on [Vercel](https://vercel.com)
3. Add environment variables
4. Deploy!

### Environment Variables for Production

Make sure to add these in your hosting platform:

```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

### Update Supabase Redirect URLs

After deployment, add your production URL to Supabase:
- `https://yourdomain.com/auth/callback`

## 📄 License

This project is part of the AI Film Studio and is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please read the main repository's contributing guidelines.

---

**Need help?** Check the [main README](../README.md) or open an issue on GitHub.
