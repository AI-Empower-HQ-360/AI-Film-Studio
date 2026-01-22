import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";

export const metadata: Metadata = {
  title: "AI Film Studio | Transform Scripts into Films",
  description: "8-engine Enterprise Studio. Transform scripts into 30–90s cinematic films in 3–5 min. FRD/NFR aligned. v0.1.0.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
