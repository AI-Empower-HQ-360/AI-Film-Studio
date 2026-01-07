import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Film Studio | Transform Scripts into Films",
  description: "AI-powered platform that transforms text scripts into cinematic short films using cutting-edge AI technology.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
