export const fetcher = async (url: string, options?: RequestInit) => {
  // 支持相对路径自动拼接 baseUrl
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || '';
  const fullUrl = url.startsWith('http') ? url : `${baseUrl}${url}`;
  let token: string | null = null;
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('token');
  }
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...Object.fromEntries(Object.entries(options?.headers || {}).map(([k, v]) => [k, String(v)])),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  const res = await fetch(fullUrl, {
    credentials: 'include', // 如需携带cookie
    ...options,
    headers,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.msg || '请求失败');
  }
  return res.json();
};

// 图片路径拼接工具
export function getImageUrl(path: string) {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || '';
  if (!path) return "/default.png";
  if (path.startsWith("http")) return path;
  return `${baseUrl}${path}`;
}
