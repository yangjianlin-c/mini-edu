"use client";
import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { getCurrentUser } from '@/api/user';
import type { UserInfo } from '@/types/user';

interface AuthState {
  user: UserInfo | null;
  token: string | null;
  loading: boolean;
}

const initialState: AuthState = { user: null, token: null, loading: true };

function reducer(state: AuthState, action: any): AuthState {
  switch (action.type) {
    case 'LOGIN':
      return { ...state, user: action.user, token: action.token, loading: false };
    case 'LOGOUT':
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
      }
      return { user: null, token: null, loading: false };
    case 'SET_USER':
      return { ...state, user: action.user, loading: false };
    case 'SET_LOADING':
      return { ...state, loading: action.loading };
    default:
      return state;
  }
}

const AuthContext = createContext<{
  user: UserInfo | null;
  loading: boolean;
  token: string | null;
  login: (user: UserInfo, token: string) => void;
  logout: () => void;
  setUser: (user: UserInfo | null) => void;
}>({
  user: null,
  loading: true,
  token: null,
  login: () => { },
  logout: () => { },
  setUser: () => { },
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  // 自动获取当前用户
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    if (token) {
      getCurrentUser()
        .then(user => dispatch({ type: 'LOGIN', user, token }))
        .catch(() => dispatch({ type: 'LOGOUT' }));
    } else {
      dispatch({ type: 'SET_LOADING', loading: false });
    }
  }, []);

  const login = (user: UserInfo, token: string) => {
    dispatch({ type: 'LOGIN', user, token });
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token);
    }
  };

  const logout = () => {
    dispatch({ type: 'LOGOUT' });
  };

  const setUser = (user: UserInfo | null) => {
    dispatch({ type: 'SET_USER', user });
  };

  return (
    <AuthContext.Provider value={{
      user: state.user,
      loading: state.loading,
      token: state.token,
      login,
      logout,
      setUser,
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
