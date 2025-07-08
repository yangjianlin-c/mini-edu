'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { login } from '@/api/user';
import { useAuth } from '@/lib/AuthContext';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { dispatch } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const res = await login(username, password);
      localStorage.setItem('token', res.token);
      dispatch({ type: 'LOGIN', user: res.user, token: res.token });
      router.push('/'); // 登录成功跳转首页
    } catch (err: any) {
      setError(err.message || '登录失败');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-sm mx-auto mt-20 space-y-4">
      <Input
        placeholder="用户名"
        value={username}
        onChange={e => setUsername(e.target.value)}
        required
      />
      <Input
        type="password"
        placeholder="密码"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
      />
      {error && <div className="text-red-500">{error}</div>}
      <Button type="submit" className="w-full">登录</Button>
    </form>
  );
}
