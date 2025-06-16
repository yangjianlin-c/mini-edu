import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/api/auth-context";


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "米克网",
  metadataBase: new URL('http://localhost:3000'),
  description: "米克网，一个分享电子产品热管理的网站。",
  openGraph: {
    images: [
      {
        url: `/og?title=${encodeURIComponent(
          "米克网"
        )}&description=${encodeURIComponent("米克网，一个分享电子产品热管理的网站。")}`,
      },
    ],
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <html lang="en">
        <body
          className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >
          {children}
        </body>
      </html>
    </AuthProvider>
  );
}
