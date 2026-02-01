'use client';

import React from 'react';
import { RoleNavigation } from '@/components/premium/RoleNavigation';

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen">
      <RoleNavigation role="admin" />
      {children}
    </div>
  );
}
