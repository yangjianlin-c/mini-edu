"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { User } from "lucide-react";
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/ui/container";
import { MainNav } from "@/components/main-nav";
import { MobileNav } from "@/components/mobile-nav";
import { ModeSwitcher } from "@/components/mode-switcher";
import { SearchBox } from "@/components/search-box";
import { Icons } from "@/components/icons";
import { useAuth } from "@/lib/AuthContext";
import { getImageUrl } from "@/lib/fetcher";

export default function SiteHeader() {
  const router = useRouter();
  const { user, loading, logout } = useAuth();

  const handleLogout = () => {
    logout();
    router.push("/");
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <Container>
        <div className="flex h-12 items-center gap-2 md:gap-3">
          <MainNav />
          <MobileNav />
          <div className="ml-auto flex items-center gap-2 md:flex-1 md:justify-end">
            <div className="hidden w-full flex-1 md:flex md:w-auto md:flex-none">
              <SearchBox />
            </div>
            <nav className="flex items-center gap-0.5">
              <Button
                asChild
                variant="ghost"
                size="icon"
                className="h-7 w-7 px-0"
              >
                <Link
                  href="https://github.com/mekesim"
                  target="_blank"
                  rel="noreferrer"
                >
                  <Icons.gitHub className="h-3.5 w-3.5" />
                  <span className="sr-only">GitHub</span>
                </Link>
              </Button>
              <ModeSwitcher />
              {user ? (
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Avatar className="h-7 w-7 cursor-pointer">
                      {user.avatar ? (
                        <AvatarImage
                          src={getImageUrl(user.avatar)}
                          alt={user.username}
                        />
                      ) : (
                        <AvatarFallback>
                          <User className="h-3.5 w-3.5" />
                        </AvatarFallback>
                      )}
                    </Avatar>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <Link href="/user/settings" className="w-full">
                      <DropdownMenuItem>个人设置</DropdownMenuItem>
                    </Link>
                    <Link href="/user/courses" className="w-full">
                      <DropdownMenuItem>我的课程</DropdownMenuItem>
                    </Link>
                    <Link href="/user/orders" className="w-full">
                      <DropdownMenuItem>我的订单</DropdownMenuItem>
                    </Link>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={handleLogout}>
                      退出登录
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              ) : (
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-7 w-7 px-0"
                    >
                      <User className="h-3.5 w-3.5" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <Link href="/auth/login" className="w-full">
                      <DropdownMenuItem>登录</DropdownMenuItem>
                    </Link>
                    <Link href="/auth/register" className="w-full">
                      <DropdownMenuItem>注册</DropdownMenuItem>
                    </Link>
                  </DropdownMenuContent>
                </DropdownMenu>
              )}
            </nav>
          </div>
        </div>
      </Container>
    </header>
  );
} 