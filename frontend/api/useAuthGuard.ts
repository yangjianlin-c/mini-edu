import { useEffect } from "react";
import { useRouter } from "next/navigation"
import { useAuth } from "./auth-context";
import { toast } from "sonner";

export default function useAuthGuard() {
  const { auth } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!auth?.token) {
      toast.error("请先登录");
      router.push("/login"); 
    }
  }, [auth, router]);
}


// 你需要在你的路由中使用这个 hook，比如：
// function ProtectedPage() {
//     useAuthGuard();
  
//     return <div>这是受保护页面内容</div>;
//   }