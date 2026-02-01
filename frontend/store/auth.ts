import { create } from 'zustand';
import { User, UserRole } from '@/types';
import { authService } from '@/services/auth';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  setUser: (user: User | null) => void;
  setIsAuthenticated: (value: boolean) => void;
  setIsLoading: (value: boolean) => void;
  setError: (error: string | null) => void;

  // Async Actions
  checkAuth: () => Promise<void>;
  logout: () => Promise<void>;
  loginWithOTP: (email: string, otp: string) => Promise<void>;

  // Helpers
  hasRole: (role: UserRole) => boolean;
  isSupervisor: () => boolean;
  isAdmin: () => boolean;
  isStudent: () => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,

  setUser: (user) => set({ user }),
  setIsAuthenticated: (value) => set({ isAuthenticated: value }),
  setIsLoading: (value) => set({ isLoading: value }),
  setError: (error) => set({ error }),

  checkAuth: async () => {
    try {
      set({ isLoading: true, error: null });
      if (authService.isAuthenticated()) {
        const response = await authService.getCurrentUser();
        if (response.data) {
          set({ user: response.data, isAuthenticated: true });
        }
      }
    } catch (error: any) {
      set({
        error: error.message || 'Failed to check authentication',
        isAuthenticated: false,
        user: null,
      });
    } finally {
      set({ isLoading: false });
    }
  },

  logout: async () => {
    try {
      await authService.logout();
      set({ user: null, isAuthenticated: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to logout' });
    }
  },

  loginWithOTP: async (email: string, otp: string) => {
    try {
      set({ isLoading: true, error: null });
      const response = await authService.verifyOTP(email, otp);
      if (response.data?.user) {
        set({ user: response.data.user, isAuthenticated: true });
      }
    } catch (error: any) {
      set({ error: error.message || 'Failed to login' });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },

  hasRole: (role: UserRole) => {
    const { user } = get();
    return user?.role === role;
  },

  isSupervisor: () => get().hasRole('SUPERVISOR'),
  isAdmin: () => get().hasRole('ADMIN'),
  isStudent: () => get().hasRole('STUDENT'),
}));
