'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { authAPI } from '@/services/api';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [adminMode, setAdminMode] = useState(false);
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleStudentLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response: any = await authAPI.login(email);
      
      if (response.message === 'OTP sent' || response.detail === 'OTP sent to email') {
        // Redirect to OTP verification
        router.push(`/auth/verify-otp?email=${encodeURIComponent(email)}`);
        toast.success('OTP sent to your email');
      } else if (response.role === 'admin') {
        setAdminMode(true);
        toast.success('Please enter your admin password');
      }
    } catch (error: any) {
      toast.error(error.detail || error.message || 'Failed to send OTP');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAdminLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response: any = await authAPI.adminLogin(email, password);
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user', JSON.stringify({
        id: response.user_id,
        email,
        name: response.name || 'Admin',
        role: response.role || 'admin',
      }));
      
      router.push('/admin/dashboard');
      toast.success('Admin login successful!');
    } catch (error: any) {
      toast.error(error.detail || 'Invalid credentials');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-blue-800 px-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            DPG Project Management
          </h1>
          <p className="text-gray-600">Sign in to your account</p>
        </div>

        <form onSubmit={adminMode ? handleAdminLogin : handleStudentLogin} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email Address
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
              placeholder="your@email.com"
              disabled={isLoading}
            />
          </div>

          {adminMode && (
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                placeholder="••••••••"
                disabled={isLoading}
              />
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full mt-6 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {isLoading ? 'Loading...' : adminMode ? 'Sign in as Admin' : 'Continue'}
          </button>
        </form>

        {adminMode && (
          <button
            onClick={() => {
              setAdminMode(false);
              setPassword('');
            }}
            className="w-full mt-4 text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            Back to Student Login
          </button>
        )}

        <div className="mt-6 text-center text-sm text-gray-600">
          <p>
            Need to request supervisor access?{' '}
            <a href="/request-access" className="text-blue-600 hover:underline">
              Apply here
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
