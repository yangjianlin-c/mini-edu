// api/auth-context.tsx
"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { userLogin, userLogout, getCourses } from "./userApi";
import { toast } from "sonner";
import type { LoginPayload, Course, ApiResponse } from "./userApi";

type User = {
    token: string;
    user: {
        username: string;
        avatar?: string;
        // 根据实际字段扩展
    };
};

interface AuthContextType {
    auth: User | null;
    courses: Course[];
    login: (payload: LoginPayload) => Promise<boolean>;
    logout: () => Promise<void>;
    getCoursesAct: (name: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [auth, setAuth] = useState<User | null>(null);
    const [courses, setCourses] = useState<Course[]>([]);

    useEffect(() => {
        if (typeof window !== "undefined") {
            const savedAuth = localStorage.getItem("auth-storage");
            if (savedAuth) {
                setAuth(JSON.parse(savedAuth));
            }
            const savedCourses = localStorage.getItem("courses-storage");
            if (savedCourses) {
                setCourses(JSON.parse(savedCourses));
            }
        }
    }, []);

    useEffect(() => {
        if (typeof window !== "undefined") {
            localStorage.setItem("auth-storage", JSON.stringify(auth));
        }
    }, [auth]);

    useEffect(() => {
        if (typeof window !== "undefined") {
            localStorage.setItem("courses-storage", JSON.stringify(courses));
        }
    }, [courses]);

    const login = async (payload: LoginPayload): Promise<boolean> => {
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

    const logout = async () => {
        await userLogout();
        setAuth(null);
        toast.success("欢迎下次回来！");
    };

    const getCoursesAct = async (name: string) => {
        const res = await getCourses(name) as ApiResponse<Course[]>;
        if (res.data) {
            setCourses(res.data);
        }
    };

    return (
        <AuthContext.Provider value={{ auth, courses, login, logout, getCoursesAct }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};
