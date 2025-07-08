import { fetcher } from '@/lib/fetcher';
import type { LoginResult } from '@/types/user';

export async function login(username: string, password: string): Promise<LoginResult> {
  return fetcher('/api/user/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
}

export async function getCurrentUser(): Promise<LoginResult['user']> {
  return fetcher('/api/user/me');
}
