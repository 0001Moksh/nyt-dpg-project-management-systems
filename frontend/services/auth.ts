import { apiClient } from './api';
import { User, AuthResponse, OTPRequest, OTPVerify } from '@/types';

export const authService = {
  // Request OTP
  async requestOTP(email: string) {
    return apiClient.post<{ message: string }>('/auth/request-otp', { email });
  },

  // Verify OTP and Login
  async verifyOTP(email: string, otp: string) {
    const response = await apiClient.post<AuthResponse>('/auth/verify-otp', {
      email,
      otp,
    });

    if (response.data?.token) {
      apiClient.setToken(response.data.token);
    }

    return response;
  },

  // Get Current User
  async getCurrentUser() {
    return apiClient.get<User>('/auth/me');
  },

  // Logout
  async logout() {
    await apiClient.post('/auth/logout', {});
    apiClient.clearToken();
  },

  // Refresh Token
  async refreshToken() {
    const response = await apiClient.post<AuthResponse>('/auth/refresh-token', {});

    if (response.data?.token) {
      apiClient.setToken(response.data.token);
    }

    return response;
  },

  // Check if token is valid
  isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem('auth_token');
  },

  // Get stored token
  getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('auth_token');
  },
};
