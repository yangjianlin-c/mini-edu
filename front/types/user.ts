export interface UserInfo {
  username: string;
  nickname?: string;
  real_name?: string;
  email?: string;
  phone?: string;
  avatar?: string;
  is_vip?: boolean;
  vip_expire_time?: string;
  // ... 其他字段
}

export interface LoginResult {
  token: string;
  user: UserInfo;
}
