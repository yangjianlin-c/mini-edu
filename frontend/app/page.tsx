"use client"

import Image from "next/image"
import Link from "next/link"
import { useEffect, useState } from "react"

import { Button } from "@/components/ui/button"
import { Container } from "@/components/ui/container"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { FileText, Ruler, Wrench } from "lucide-react"
import { listCourses } from "@/api/course"
import type { Course } from "@/types/course"
import { getImageUrl } from '@/api/config';
import CourseGrid from '@/components/CourseGrid';

export default function IndexPage() {
    const [courses, setCourses] = useState<Course[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const response = await listCourses();
                setCourses(response.map(course => ({
                    ...course,
                    image: getImageUrl(course.image)
                })));
                setError(null);
            } catch (err) {
                setError('获取课程列表失败');
                console.error('获取课程列表失败:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchCourses();
    }, []);

    return (
        <>
            <SiteHeader />
            <main className="flex-1">
                <section>
                    <Container>
                        <div className="grid grid-cols-1 md:grid-cols-[6fr_6fr] gap-4 py-8">
                            <div className="flex flex-col justify-center space-y-4">
                                <h1 className="font-heading text-3xl sm:text-5xl md:text-6xl lg:text-7xl">
                                    米克网
                                </h1>
                                <p className="leading-normal text-muted-foreground sm:text-lg sm:leading-7">
                                    我们提供专业的电子产品热管理解决方案，帮助您的产品获得最佳性能和可靠性。从散热设计到热分析，我们都能为您提供全方位的支持。
                                </p>
                                <div className="space-x-4  space-y-4">
                                    <Button asChild size="lg">
                                        <Link href="/courses">在线课程</Link>
                                    </Button>
                                    <Button asChild size="lg" variant="outline">
                                        <Link href="/tools/unit-converter">在线工具</Link>
                                    </Button>
                                </div>
                            </div>
                            <div className="flex items-center justify-center max-w-[400px] mx-auto">
                                <Image
                                    src="/lady.svg"
                                    alt="热管理解决方案"
                                    width={300}
                                    height={240}
                                    className="w-full organic-radius"
                                    loading="lazy"
                                />
                            </div>
                        </div>
                    </Container>
                </section>

                <section>
                    <Container className="space-y-6 py-8 md:py-12 lg:py-24">
                        <div className="mx-auto flex max-w-[58rem] flex-col items-center space-y-4 text-center">
                            <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl pb-8">
                                在线课程
                            </h2>
                        </div>

                        {/* 使用 CourseGrid 组件来渲染课程 */}
                        {loading ? (
                            <div className="col-span-3 text-center py-8">加载中...</div>
                        ) : error ? (
                            <div className="col-span-3 text-center py-8 text-red-500">{error}</div>
                        ) : courses.length === 0 ? (
                            <div className="col-span-3 text-center py-8">暂无课程</div>
                        ) : (
                            <CourseGrid courses={courses} />
                        )}
                    </Container>
                </section>

                <section>
                    <Container className="space-y-6 py-8 md:py-12">
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
                    </Container>
                </section>
            </main>
            <SiteFooter />
        </>
    )
}
