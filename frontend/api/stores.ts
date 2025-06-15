import { useState, useEffect } from "react";
import { getCourses, userLogin, userLogout } from "./userApi";
import { toast } from "sonner";
import type { LoginPayload, Course, ApiResponse } from "./userApi";

type User = {
  token: string;
  user: {
    username: string;
    // 其他字段可继续扩展
  };
};

type AuthState = {
  auth: User | null;
  courses: Course[];
  setAuth: (newAuth: User | null) => void;
  loginAct: (payload: LoginPayload) => Promise<boolean>;
  logoutAct: () => Promise<void>;
  getCoursesAct: (name: string) => Promise<void>;
};

export const useTokenStore = (): AuthState => {
  const [auth, setAuth] = useState<User | null>(() => {
    const savedAuth = localStorage.getItem("auth-storage");
    return savedAuth ? JSON.parse(savedAuth) : null;
  });

  const [courses, setCourses] = useState<Course[]>(() => {
    const savedCourses = localStorage.getItem("courses-storage");
    return savedCourses ? JSON.parse(savedCourses) : [];
  });

  useEffect(() => {
    localStorage.setItem("auth-storage", JSON.stringify(auth));
  }, [auth]);

  useEffect(() => {
    localStorage.setItem("courses-storage", JSON.stringify(courses));
  }, [courses]);

  const loginAct = async (payload: LoginPayload): Promise<boolean> => {
    try {
      const res = await userLogin(payload) as ApiResponse<User>;
      if (res.status !== 200) {
        toast.error("登录失败，请检查账号密码");
        return false;
      }
      if (res.data?.token) {
        setAuth(res.data);
        toast.success("欢迎回来！" + res.data.user.username);
        return true;
      } else {
        toast.error("登录响应格式异常");
        return false;
      }
    } catch (err) {
      toast.error("网络错误，无法登录");
      return false;
    }
  };

  const logoutAct = async (): Promise<void> => {
    await userLogout();
    setAuth(null);
    toast.success("欢迎下次回来！");
  };

  const getCoursesAct = async (name: string): Promise<void> => {
    const res = await getCourses(name) as ApiResponse<Course[]>;
    if (res.data) {
      setCourses(res.data);
    }
  };

  return {
    auth,
    courses,
    setAuth,
    loginAct,
    logoutAct,
    getCoursesAct,
  };
};
