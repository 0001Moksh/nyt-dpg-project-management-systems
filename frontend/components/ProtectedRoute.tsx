'use client';

import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { useEffect } from 'react';

export default function ProtectedRoute({ children, requiredRole }: {
  children: React.ReactNode;
  requiredRole?: string;
}) {
  const { user, token } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!token || !user) {
      router.push('/auth/login');
      return;
    }

    if (requiredRole && user.role !== requiredRole) {
      router.push('/');
    }
  }, [token, user, requiredRole, router]);

  if (!token || !user) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (requiredRole && user.role !== requiredRole) {
    return <div className="flex items-center justify-center min-h-screen">Unauthorized</div>;
  }

  return <>{children}</>;
}
