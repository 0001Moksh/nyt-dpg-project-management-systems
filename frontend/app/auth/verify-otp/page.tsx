'use client';

import React from "react"

import { useState, FormEvent, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuthStore } from '@/store/auth';
import { authService } from '@/services/auth';
import Link from 'next/link';

function OTPVerifyContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const email = searchParams?.get('email') || '';

  const setUser = useAuthStore((state) => state.setUser);
  const setIsAuthenticated = useAuthStore((state) => state.setIsAuthenticated);

  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes

  // Countdown timer
  useEffect(() => {
    const interval = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleOtpChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.replace(/\D/g, '').slice(0, 6);
    setOtp(value);
    setError('');
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (!otp || otp.length !== 6) {
        setError('Please enter a valid 6-digit OTP');
        setLoading(false);
        return;
      }

      if (!email) {
        setError('Email not found. Please start over.');
        setLoading(false);
        router.push('/auth/login');
        return;
      }

      // Verify OTP
      const response = await authService.verifyOTP(email, otp);

      if (response.success && response.data?.user) {
        // Store user in state
        setUser(response.data.user);
        setIsAuthenticated(true);

        // Redirect based on role
        setTimeout(() => {
          const redirectPath =
            response.data.user.role === 'STUDENT'
              ? '/student/dashboard'
              : response.data.user.role === 'SUPERVISOR'
                ? '/supervisor/dashboard'
                : '/admin/dashboard';

          router.push(redirectPath);
        }, 500);
      } else {
        setError(response.error || 'Invalid OTP. Please try again.');
      }
    } catch (err: any) {
      console.error('[v0] OTP verification error:', err);
      setError(
        err.response?.data?.message ||
          err.message ||
          'Verification failed. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleResendOTP = async () => {
    try {
      setLoading(true);
      const response = await authService.requestOTP(email);

      if (response.success) {
        setOtp('');
        setError('');
        setTimeLeft(300);
      } else {
        setError('Failed to resend OTP');
      }
    } catch (err: any) {
      setError('Failed to resend OTP');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-light to-background px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-primary mb-2">Verify OTP</h1>
          <p className="text-muted">
            Enter the 6-digit code sent to{' '}
            <span className="font-semibold">{email}</span>
          </p>
        </div>

        {/* Card */}
        <div className="card shadow-lg">
          <div className="card-content">
            {/* Error Message */}
            {error && (
              <div className="alert alert-danger mb-6 animate-fade-in">
                {error}
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* OTP Input */}
              <div>
                <label htmlFor="otp" className="form-label">
                  One-Time Password
                </label>
                <input
                  id="otp"
                  type="text"
                  name="otp"
                  value={otp}
                  onChange={handleOtpChange}
                  placeholder="000000"
                  maxLength={6}
                  required
                  disabled={loading || timeLeft === 0}
                  className="w-full text-center text-2xl letter-spacing-2 font-mono tracking-widest"
                  aria-label="One-time password"
                />
                <p className="text-xs text-muted mt-2">
                  Check your email for the verification code
                </p>
              </div>

              {/* Timer */}
              <div className="flex items-center justify-between p-3 bg-surface rounded-md border border-border">
                <span className="text-sm text-muted">Time remaining:</span>
                <span
                  className={`text-lg font-mono font-semibold ${
                    timeLeft < 60 ? 'text-danger' : 'text-primary'
                  }`}
                >
                  {formatTime(timeLeft)}
                </span>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading || !otp || timeLeft === 0}
                className="w-full btn btn-primary py-3 font-semibold"
              >
                {loading ? 'Verifying...' : 'Verify OTP'}
              </button>
            </form>

            {/* Divider */}
            <div className="relative my-6">
              <div className="divider"></div>
              <div className="absolute inset-x-0 -top-3 flex justify-center">
                <span className="bg-background px-2 text-xs text-muted">
                  didn't receive?
                </span>
              </div>
            </div>

            {/* Resend OTP */}
            <button
              onClick={handleResendOTP}
              disabled={loading || timeLeft > 0}
              className="w-full btn btn-outline py-2 font-semibold"
            >
              Resend OTP
            </button>
          </div>

          {/* Footer */}
          <div className="card-footer bg-surface text-center">
            <Link
              href="/auth/login"
              className="text-primary hover:underline text-sm"
            >
              ← Back to Login
            </Link>
          </div>
        </div>

        {/* Footer Text */}
        <div className="text-center mt-6 text-sm text-muted">
          <p>
            Having trouble?{' '}
            <a
              href="https://nexyugtech.com/support"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >
              Contact Support
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default function OTPVerifyPage() {
  return (
    <Suspense>
      <OTPVerifyContent />
    </Suspense>
  );
}
