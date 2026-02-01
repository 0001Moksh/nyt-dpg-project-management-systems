'use client';

import { useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  useEffect(() => {
    // Hydrate auth store on mount
    useAuthStore.getState().hydrate();
  }, []);

  return (
    <html lang="en">
      <head>
        <title>DPG Project Management System</title>
        <meta name="description" content="DPG Project Management System" />
      </head>
      <body className="bg-gray-50">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  );
}
