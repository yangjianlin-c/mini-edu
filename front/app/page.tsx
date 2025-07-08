"use client";
import React, { useEffect, useState } from "react";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import SiteHeader from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText, Ruler, Wrench } from "lucide-react";
import { fetcher, getImageUrl } from "@/lib/fetcher";

export default function HomePage() {
  const [courses, setCourses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetcher("/api/course/feature")
      .then(setCourses)
      .catch(() => setError("获取课程失败"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <>
      <SiteHeader />
      <main className="flex-1">
        {/* 顶部介绍区块 */}
        <section>
          <div className="mx-auto w-full max-w-[1400px] px-4 md:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-[6fr_6fr] gap-4 py-8">
              <div className="flex flex-col justify-center space-y-4">
                <h1 className="font-heading text-3xl sm:text-5xl md:text-6xl lg:text-7xl">
                  米克网
                </h1>
                <p className="leading-normal text-muted-foreground sm:text-lg sm:leading-7">
                  我们提供专业的电子产品热管理解决方案，帮助您的产品获得最佳性能和可靠性。从散热设计到热分析，我们都能为您提供全方位的支持。
                </p>
                <div className="space-x-4 space-y-4">
                  <Button asChild size="lg">
                    <Link href="/courses">在线课程</Link>
                  </Button>
                  <Button asChild size="lg" variant="outline">
                    <Link href="/tools/unit-converter">在线工具</Link>
                  </Button>
                </div>
              </div>
              <div className="flex items-center justify-center max-w-[400px] mx-auto">
                <div
                  className="overflow-hidden"
                  style={{
                    borderRadius: "63% 37% 30% 70% / 50% 45% 55% 50%"
                  }}
                >
                  <Image
                    src="/lady.svg"
                    alt="热管理解决方案"
                    width={300}
                    height={240}
                    className="w-full"
                    loading="lazy"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 课程区块 */}
        <section>
          <div className="mx-auto w-full max-w-[1400px] px-4 md:px-6 lg:px-8 space-y-6 py-8 md:py-12 lg:py-24">
            <div className="mx-auto flex max-w-[58rem] flex-col items-center space-y-4 text-center">
              <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl pb-8">
                在线课程
              </h2>
            </div>
            {loading ? (
              <div className="text-center py-8">加载中...</div>
            ) : error ? (
              <div className="text-center py-8 text-red-500">{error}</div>
            ) : courses.length === 0 ? (
              <div className="text-center py-8">暂无课程</div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                {courses.map((course) => (
                  <Card key={course.id} className="flex flex-col group">
                    <Link href={`/course/${course.id}`} className="block overflow-hidden rounded-t-md">
                      <Image
                        src={getImageUrl(course.image)}
                        alt={course.title}
                        width={400}
                        height={200}
                        className="object-cover h-48 w-full transition-transform duration-200 group-hover:scale-105 group-hover:shadow-lg"
                      />
                    </Link>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Link href={`/course/${course.id}`} className="hover:text-primary hover:underline transition-colors duration-200">
                          {course.title}
                        </Link>
                      </CardTitle>
                      <CardDescription>{course.description}</CardDescription>
                    </CardHeader>
                    <CardFooter className="mt-auto flex flex-col items-start gap-2">
                      <div className="flex gap-2 flex-wrap">
                        {course.tags && course.tags.map((tag: any) => (
                          <span key={tag.id} className="bg-gray-100 text-xs px-2 py-0.5 rounded text-gray-600">
                            {tag.name}
                          </span>
                        ))}
                      </div>
                      <div className="text-lg font-bold text-primary">
                        {course.price === 0 ? "免费" : `¥${course.price}`}
                      </div>
                      <Button asChild size="sm" className="mt-2">
                        <Link href={`/course/${course.id}`}>查看详情</Link>
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </section>

        {/* 工具区块 */}
        <section>
          <div className="mx-auto w-full max-w-[1400px] px-4 md:px-6 lg:px-8 space-y-6 py-8 md:py-12">
            <div className="mx-auto flex max-w-[58rem] flex-col items-center space-y-4 text-center">
              <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl pb-8">
                在线工具
              </h2>
            </div>
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
              <Card>
                <div className="flex flex-col items-center p-6 h-full">
                  <Ruler className="h-12 w-12 mb-4" />
                  <CardHeader className="p-0 text-center w-full">
                    <CardTitle className="text-2xl mb-2">单位转换</CardTitle>
                    <CardDescription>
                      快速转换各种热管理相关的物理单位
                    </CardDescription>
                  </CardHeader>
                  <CardFooter className="mt-auto pt-6">
                    <Button asChild>
                      <Link href="/tools/unit-converter">开始使用</Link>
                    </Button>
                  </CardFooter>
                </div>
              </Card>

              <Card>
                <div className="flex flex-col items-center p-6 h-full">
                  <FileText className="h-12 w-12 mb-4" />
                  <CardHeader className="p-0 text-center w-full">
                    <CardTitle className="text-2xl mb-2">Markdown 编辑器</CardTitle>
                    <CardDescription>
                      在线编写和预览 Markdown 文档
                    </CardDescription>
                  </CardHeader>
                  <CardFooter className="mt-auto pt-6">
                    <Button asChild>
                      <Link href="/tools/mdeditor">开始使用</Link>
                    </Button>
                  </CardFooter>
                </div>
              </Card>

              <Card>
                <div className="flex flex-col items-center p-6 h-full">
                  <Wrench className="h-12 w-12 mb-4" />
                  <CardHeader className="p-0 text-center w-full">
                    <CardTitle className="text-2xl mb-2">更多工具</CardTitle>
                    <CardDescription>
                      更多实用工具正在开发中...
                    </CardDescription>
                  </CardHeader>
                  <CardFooter className="mt-auto pt-6">
                    <Button variant="outline" disabled>
                      敬请期待
                    </Button>
                  </CardFooter>
                </div>
              </Card>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
