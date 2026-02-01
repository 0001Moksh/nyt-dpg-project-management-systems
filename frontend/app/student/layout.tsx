'use client';

import React from 'react';
import { RoleNavigation } from '@/components/premium/RoleNavigation';

export default function StudentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen">
      <RoleNavigation role="student" />
      {children}
    </div>
  );
}
