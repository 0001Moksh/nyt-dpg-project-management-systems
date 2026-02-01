import React from "react"
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'DPG Project Management System',
  description:
    'A comprehensive project management system for DPG ITM College by NexyugTech',
  keywords: [
    'project management',
    'education',
    'dpg',
    'itm',
    'college',
  ],
  authors: [{ name: 'NexyugTech', url: 'https://nexyugtech.com' }],
  creator: 'NexyugTech',
  publisher: 'DPG ITM College',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://dpg-pms.com',
    siteName: 'DPG Project Management System',
    images: [
      {
        url: 'https://dpg-pms.com/og-image.png',
        width: 1200,
        height: 630,
        alt: 'DPG Project Management System',
      },
    ],
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
};

export const viewport = {
  themeColor: '#007bff',
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body
        className={`${inter.className} bg-background text-foreground antialiased`}
      >
        <main>{children}</main>
      </body>
    </html>
  );
}
