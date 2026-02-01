'use client';

import React from 'react';
import { RoleNavigation } from '@/components/premium/RoleNavigation';

export default function AccountantLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen">
      <RoleNavigation role="accountant" />
      {children}
    </div>
  );
}
