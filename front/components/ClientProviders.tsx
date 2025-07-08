"use client";
import { SWRConfig } from "swr";
import { fetcher } from "@/lib/fetcher";
import { AuthProvider } from "@/lib/AuthContext";

export default function ClientProviders({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <SWRConfig value={{ fetcher }}>
        {children}
      </SWRConfig>
    </AuthProvider>
  );
}
