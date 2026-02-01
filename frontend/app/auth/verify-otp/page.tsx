'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import toast from 'react-hot-toast';
import { authAPI } from '@/services/api';
import { useAuthStore } from '@/store/authStore';

export default function VerifyOTPPage() {
  const [otp, setOtp] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [email, setEmail] = useState('');
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes
  const router = useRouter();
  const searchParams = useSearchParams();
  const { setToken, setUser } = useAuthStore();

  useEffect(() => {
    const emailParam = searchParams.get('email');
    if (emailParam) {
      setEmail(decodeURIComponent(emailParam));
    }
  }, [searchParams]);

  useEffect(() => {
    if (timeLeft <= 0) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (otp.length !== 6) {
        toast.error('OTP must be 6 digits');
        return;
      }

      const response: any = await authAPI.verifyOtp(email, otp);
      
      // Store token and user info
      setToken(response.access_token);
      setUser({
        id: response.user_id,
        email,
        name: response.name || 'User',
        role: response.role || 'student',
      });

      // Redirect based on role
      switch (response.role) {
        case 'admin':
          router.push('/admin/dashboard');
          break;
        case 'supervisor':
          router.push('/supervisor/dashboard');
          break;
        case 'student':
          router.push('/student/dashboard');
          break;
        default:
          router.push('/');
      }

      toast.success('Login successful!');
    } catch (error: any) {
      toast.error(error.detail || 'Invalid OTP');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-blue-800 px-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Verify OTP
          </h1>
          <p className="text-gray-600">
            Enter the 6-digit code sent to {email}
          </p>
        </div>

        <form onSubmit={handleVerifyOTP} className="space-y-4">
          <div>
            <label htmlFor="otp" className="block text-sm font-medium text-gray-700">
              One-Time Password
            </label>
            <input
              type="text"
              id="otp"
              value={otp}
              onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
              maxLength={6}
              placeholder="000000"
              className="mt-1 w-full px-4 py-2 text-center text-2xl border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent font-mono tracking-widest"
              disabled={isLoading || timeLeft <= 0}
            />
          </div>

          <div className="text-center">
            <p className="text-sm text-gray-600">
              OTP expires in:{' '}
              <span className={timeLeft < 60 ? 'text-red-600 font-bold' : 'text-gray-900 font-bold'}>
                {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, '0')}
              </span>
            </p>
          </div>

          <button
            type="submit"
            disabled={isLoading || otp.length !== 6 || timeLeft <= 0}
            className="w-full mt-6 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {isLoading ? 'Verifying...' : 'Verify OTP'}
          </button>
        </form>

        <div className="mt-6">
          <button
            onClick={() => router.push('/auth/login')}
            className="w-full text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            Back to Login
          </button>
        </div>
      </div>
    </div>
  );
}
