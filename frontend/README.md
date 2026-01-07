# AI Film Studio Frontend

A modern, production-ready Next.js 14 application with Supabase authentication.

## 🚀 Features

- ✅ **Next.js 14** with App Router
- ✅ **TypeScript** for type safety
- ✅ **Tailwind CSS** for styling
- ✅ **Supabase Authentication** with email/password
- ✅ **Protected Routes** with middleware
- ✅ **Server & Client Components** optimized for performance
- ✅ **Responsive Design** works on all devices

## 📋 Prerequisites

- Node.js 18+ 
- npm or yarn
- Supabase account (configured below)

## 🛠️ Installation

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.local.example .env.local
```

The `.env.local` file should contain:

```env
NEXT_PUBLIC_SUPABASE_URL=https://spfefoaeyowaojgqtxxo.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_oDObTtUno0j_-7Pz_gAaaw_KHe4vF-q
SUPABASE_SERVICE_ROLE_KEY=sb_secret_Gnf6P-g42GzzfckiFu9gkw_E4lO8Oem
```

### 3. Set Up Supabase Database

Go to your Supabase project dashboard (https://spfefoaeyowaojgqtxxo.supabase.co) and run the following SQL in the SQL Editor:

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

-- Create policies
CREATE POLICY "Users can view own profile" 
  ON profiles FOR SELECT 
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" 
  ON profiles FOR UPDATE 
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" 
  ON profiles FOR INSERT 
  WITH CHECK (auth.uid() = id);

-- Create function to handle new user creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email) 
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user signup
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW 
  EXECUTE FUNCTION public.handle_new_user();
```

### 4. Configure Supabase Email Settings

1. Go to your Supabase Dashboard → Authentication → Email Templates
2. Make sure email confirmation is enabled or disabled based on your needs
3. For development, you can disable email confirmation:
   - Go to Authentication → Settings
   - Scroll to "Email Auth"
   - Toggle "Enable email confirmations" OFF (for development only)

### 5. Configure Supabase Site URL

1. Go to Authentication → URL Configuration
2. Set Site URL to: `http://localhost:3000`
3. Add Redirect URLs:
   - `http://localhost:3000/auth/callback`
   - `http://localhost:3000/dashboard`

## 🚀 Running the Application

### Development Mode

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build

```bash
npm run build
npm start
```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout with metadata
│   ├── page.tsx                # Landing page
│   ├── login/
│   │   └── page.tsx            # Login page
│   ├── signup/
│   │   └── page.tsx            # Signup page
│   ├── dashboard/
│   │   └── page.tsx            # Protected dashboard
│   ├── auth/
│   │   └── callback/
│   │       └── route.ts        # Auth callback handler
│   └── globals.css             # Global styles
├── components/
│   └── auth/
│       ├── SignInForm.tsx      # Login form component
│       ├── SignUpForm.tsx      # Signup form component
│       └── SignOutButton.tsx   # Logout button
├── lib/
│   └── supabase/
│       ├── client.ts           # Browser Supabase client
│       ├── server.ts           # Server Supabase client
│       └── middleware.ts       # Session management
├── types/
│   └── supabase.ts             # TypeScript types
├── middleware.ts               # Next.js middleware
├── .env.local.example          # Environment template
├── .gitignore                  # Git ignore
├── next.config.js              # Next.js config
├── package.json                # Dependencies
├── postcss.config.js           # PostCSS config
├── tailwind.config.ts          # Tailwind config
├── tsconfig.json               # TypeScript config
└── README.md                   # This file
```

## 🔐 Authentication Flow

### Sign Up Flow

1. User visits `/signup`
2. Fills out email and password form
3. Supabase creates user account
4. User receives confirmation email (if enabled)
5. User clicks confirmation link
6. Redirected to `/dashboard`

### Sign In Flow

1. User visits `/login`
2. Enters credentials
3. Supabase validates credentials
4. User redirected to `/dashboard`
5. Session maintained via cookies

### Protected Routes

The dashboard route (`/dashboard`) is protected:
- Server component checks authentication
- Redirects to `/login` if not authenticated
- Uses Supabase server client for SSR

## 🎨 Styling

The application uses Tailwind CSS with a custom blue primary color scheme:

- Primary: Blue (#3b82f6)
- Forms: Clean, modern design
- Responsive: Mobile-first approach
- Accessible: WCAG compliant

## 🔧 Configuration Files

### next.config.js

Basic Next.js configuration with React strict mode enabled.

### tailwind.config.ts

Tailwind configured with custom primary color palette and content paths.

### tsconfig.json

TypeScript configured with strict mode and path aliases (`@/*` → `./`).

### middleware.ts

Next.js middleware that:
- Refreshes Supabase sessions on every request
- Runs on all routes (except static assets)
- Maintains authentication state

## 🧪 Testing the Application

### Manual Testing Checklist

1. **Landing Page** (`/`)
   - ✅ Displays hero section
   - ✅ Shows features
   - ✅ Login/Signup buttons work

2. **Sign Up** (`/signup`)
   - ✅ Form validation works
   - ✅ Password confirmation works
   - ✅ Success message shows
   - ✅ Email sent (if confirmations enabled)

3. **Sign In** (`/login`)
   - ✅ Valid credentials work
   - ✅ Invalid credentials show error
   - ✅ Redirects to dashboard

4. **Dashboard** (`/dashboard`)
   - ✅ Shows user email and ID
   - ✅ Protected (redirects if not authenticated)
   - ✅ Sign out button works

5. **Sign Out**
   - ✅ Clears session
   - ✅ Redirects to login

## 🐛 Troubleshooting

### "Invalid JWT" or "Session not found"

Clear cookies and sign in again. This can happen during development.

### Email confirmation not working

1. Check Supabase email settings
2. For development, disable email confirmations in Supabase settings
3. Check spam folder

### Redirect not working

1. Verify Site URL in Supabase settings
2. Check redirect URLs are whitelisted
3. Clear browser cache

### Build errors

```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues or questions:
- Create an issue in the GitHub repository
- Check the Supabase documentation
- Review the Next.js documentation

---

**Built with ❤️ using Next.js 14 and Supabase**
