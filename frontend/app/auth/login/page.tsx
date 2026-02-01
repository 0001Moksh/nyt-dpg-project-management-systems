'use client';

import { useState, FormEvent, ChangeEvent } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth';
import Link from 'next/link';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleEmailChange = (e: ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
    setError('');
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Validate email
      if (!email || !email.includes('@')) {
        setError('Please enter a valid email address');
        setLoading(false);
        return;
      }

      // Request OTP
      const response = await authService.requestOTP(email);

      if (response.success) {
        setSuccess(true);
        // Redirect to OTP verification after 2 seconds
        setTimeout(() => {
          router.push(`/auth/verify-otp?email=${encodeURIComponent(email)}`);
        }, 1500);
      } else {
        setError(response.error || 'Failed to send OTP. Please try again.');
      }
    } catch (err: any) {
      console.error('[v0] Login error:', err);
      setError(
        err.response?.data?.message ||
          err.message ||
          'An error occurred. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-light to-background px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-primary mb-2">DPG PMS</h1>
          <p className="text-muted">Project Management System</p>
          <p className="text-sm text-muted mt-1">DPG ITM College</p>
        </div>

        {/* Card */}
        <div className="card shadow-lg">
          <div className="card-content">
            {/* Success Message */}
            {success && (
              <div className="alert alert-success mb-6 animate-fade-in">
                OTP sent successfully! Redirecting...
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="alert alert-danger mb-6 animate-fade-in">
                {error}
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="form-label">
                  Email Address
                </label>
                <input
                  id="email"
                  type="email"
                  name="email"
                  value={email}
                  onChange={handleEmailChange}
                  placeholder="you@dpg-itm.edu.in"
                  required
                  disabled={loading || success}
                  className="w-full"
                  aria-label="Email address"
                />
                <p className="text-xs text-muted mt-1">
                  We will send a one-time password to this email
                </p>
              </div>

              <button
                type="submit"
                disabled={loading || success || !email}
                className="w-full btn btn-primary py-3 font-semibold"
              >
                {loading ? 'Sending OTP...' : 'Send OTP'}
              </button>
            </form>

            {/* Divider */}
            <div className="relative my-6">
              <div className="divider"></div>
              <div className="absolute inset-x-0 -top-3 flex justify-center">
                <span className="bg-background px-2 text-xs text-muted">
                  or
                </span>
              </div>
            </div>

            {/* Demo Credentials */}
            <div className="bg-surface p-4 rounded-md border border-border">
              <p className="text-xs font-semibold text-foreground mb-2">
                Demo Credentials:
              </p>
              <div className="space-y-1 text-xs text-muted">
                <p>
                  <strong>Student:</strong> student@dpg-itm.edu.in
                </p>
                <p>
                  <strong>Supervisor:</strong> supervisor@dpg-itm.edu.in
                </p>
                <p>
                  <strong>Admin:</strong> admin@dpg-itm.edu.in
                </p>
                <p className="mt-2 pt-2 border-t border-border">
                  OTP: Check backend console (development)
                </p>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="card-footer bg-surface text-center text-xs text-muted">
            <p>
              By logging in, you agree to our{' '}
              <Link href="/terms" className="text-primary hover:underline">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link href="/privacy" className="text-primary hover:underline">
                Privacy Policy
              </Link>
            </p>
          </div>
        </div>

        {/* Footer Text */}
        <div className="text-center mt-6 text-sm text-muted">
          <p>
            Powered by{' '}
            <a
              href="https://nexyugtech.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >
              NexyugTech
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
