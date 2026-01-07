import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Film Studio',
  description: 'Create films with AI - Script to Video',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
