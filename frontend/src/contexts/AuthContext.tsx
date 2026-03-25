import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from '../api/client';

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, confirmPassword: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
  showToast: (message: string, type: 'success' | 'error' | 'info') => void;
  toast: { message: string; type: 'success' | 'error' | 'info' } | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true); // Start as loading to check auth first
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);

  const showToast = (message: string, type: 'success' | 'error' | 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 5000);
  };

  const checkAuth = async () => {
    const token = localStorage.getItem('authToken');
    if (token) {
      try {
        const response = await apiClient.get('/profile');
        setUser({ id: response.data.email, email: response.data.email }); // Adjust ID mapping depending on API response if id isn't there
      } catch (error) {
        console.error('Auth verification failed', error);
        localStorage.removeItem('authToken');
        setUser(null);
      }
    }
    setLoading(false);
  };

  useEffect(() => {
    checkAuth();
    
    // Listen for unauthorized events to gracefully logout
    const handleUnauthorized = () => {
      setUser(null);
      showToast('Session expired. Please log in again.', 'error');
    };
    window.addEventListener('auth:unauthorized', handleUnauthorized);
    return () => window.removeEventListener('auth:unauthorized', handleUnauthorized);
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await apiClient.post('/login', { email, password });
      const data = response.data;
      localStorage.setItem('authToken', data.access_token);
      await checkAuth();
      showToast('Successfully logged in!', 'success');
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Invalid credentials';
      showToast(msg, 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string, confirmPassword: string) => {
    if (password !== confirmPassword) {
      showToast('Passwords do not match', 'error');
      throw new Error('Passwords do not match');
    }

    if (password.length < 6) {
      showToast('Password must be at least 6 characters', 'error');
      throw new Error('Password too short');
    }

    setLoading(true);
    try {
      const response = await apiClient.post('/register', { email, password, confirmPassword });
      const data = response.data;
      localStorage.setItem('authToken', data.access_token);
      await checkAuth();
      showToast('Account created successfully!', 'success');
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Registration failed';
      showToast(msg, 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('authToken');
    showToast('Logged out successfully', 'info');
  };

  const value = {
    user,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    loading,
    showToast,
    toast,
  };

  return <AuthContext.Provider value={value}>{!loading && children}</AuthContext.Provider>;
}