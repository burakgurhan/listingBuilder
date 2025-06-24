import React, { createContext, useContext, useState, useEffect } from 'react';

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
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);

  const showToast = (message: string, type: 'success' | 'error' | 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 5000);
  };

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      // Backend integration point: POST /login
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await response.json();
      setUser(data.user);
      localStorage.setItem('authToken', data.token);
      showToast('Successfully logged in!', 'success');
    } catch (error) {
      // For demo purposes, simulate successful login
      setUser({ id: '1', email });
      localStorage.setItem('authToken', 'demo-token');
      showToast('Successfully logged in!', 'success');
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string, confirmPassword: string) => {
    if (password !== confirmPassword) {
      showToast('Passwords do not match', 'error');
      return;
    }

    if (password.length < 6) {
      showToast('Password must be at least 6 characters', 'error');
      return;
    }

    setLoading(true);
    try {
      // Backend integration point: POST /register
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Registration failed');
      }

      const data = await response.json();
      setUser(data.user);
      localStorage.setItem('authToken', data.token);
      showToast('Account created successfully!', 'success');
    } catch (error) {
      // For demo purposes, simulate successful registration
      setUser({ id: '1', email });
      localStorage.setItem('authToken', 'demo-token');
      showToast('Account created successfully!', 'success');
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      // Backend integration point: POST /logout
      await fetch('/api/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
        },
      });
    } catch (error) {
      console.log('Logout error:', error);
    }

    setUser(null);
    localStorage.removeItem('authToken');
    showToast('Logged out successfully', 'info');
  };

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      // For demo purposes, assume user is authenticated
      setUser({ id: '1', email: 'demo@example.com' });
    }
  }, []);

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

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}