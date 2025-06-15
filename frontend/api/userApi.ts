import api from "./req";
import { AxiosResponse } from "axios";

// 统一 API 响应类型
interface ApiResponseData<T = any> {
  status: number;
  data?: T;
}

export type ApiResponse<T = any> = AxiosResponse<ApiResponseData<T>>;

// ---------------- 接口参数类型 ----------------

export interface LoginPayload {
  username: string;
  password: string;
}

export interface Course {
  id: number;
  name: string;
  description: string;
  coverUrl: string;
  price: number;
  // 根据实际字段再补充
}

export interface FeedbackPayload {
  message: string;
  contact?: string;
}

// ---------------- API 方法封装 ----------------

// 获取轮播图
export function getBanners(): Promise<ApiResponse<string[]>> {
  return api({
    method: "GET",
    url: "/user/banner",
  });
}

// 获取所有课程
export function getCourses(name: string): Promise<ApiResponse<Course[]>> {
  return api({
    method: "GET",
    url: "/course/all",
    params: { name },
  });
}

// 用户登录
export function userLogin(payload: LoginPayload): Promise<ApiResponse> {
  return api({
    method: "POST",
    data: payload,
    url: "/user/login",
  });
}

// 用户登出
export function userLogout(): Promise<ApiResponse> {
  return api({
    method: "POST",
    url: "/user/logout",
  });
}

// 上传用户头像
export function userAvatar(data: FormData): Promise<ApiResponse> {
  return api({
    method: "POST",
    url: "/user/avatar",
    headers: {
      "Content-Type": "multipart/form-data",
    },
    data,
  });
}

// 修改用户密码
export function changePsd(password: string): Promise<ApiResponse> {
  return api({
    method: "PATCH",
    url: "/user/profile",
    data: { password },
  });
}

// 用户反馈
export function addMsg(data: FeedbackPayload): Promise<ApiResponse> {
  return api({
    method: "POST",
    url: "/user/feedback",
    data,
  });
}
