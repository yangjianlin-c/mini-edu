"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Container } from "@/components/ui/container"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import { listCourses, listTags } from "@/api/course"
import { Course, CourseTag } from "@/types/course";
import { getImageUrl } from '@/api/config';
import CourseGrid from '@/components/CourseGrid';

interface CoursesPageProps {
    params?: { [key: string]: string | string[] | undefined }
    searchParams?: { [key: string]: string | string[] | undefined }
}

export default function CoursesPage({ params, searchParams }: CoursesPageProps) {
    const [courses, setCourses] = useState<Course[]>([])
    const [tags, setTags] = useState<CourseTag[]>([])
    const [loading, setLoading] = useState(true)
    const [selectedTagId, setSelectedTagId] = useState<number | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [coursesResponse, tagsResponse] = await Promise.all([
                    listCourses(undefined, selectedTagId || undefined),
                    listTags()
                ]);

                setCourses(
                    Array.isArray(coursesResponse)
                        ? coursesResponse.map(course => ({
                            ...course,
                            image: getImageUrl(course.image)
                        }))
                        : []
                );

                setTags(Array.isArray(tagsResponse) ? tagsResponse : []);

            } catch (error) {
                console.error("获取数据失败:", error);
                setCourses([]);
                setTags([]);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [selectedTagId]);

    return (
        <>
            <SiteHeader />
            <main className="flex-1">
                <Container className="space-y-6 py-8 md:py-12">
                    <div className="mx-auto flex max-w-[58rem] flex-col items-center space-y-4 text-center">
                        <h1 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl">
                            在线课程
                        </h1>
                        <p className="max-w-[85%] leading-normal text-muted-foreground sm:text-lg sm:leading-7">
                            米克网提供的电子产品热管理在线课程
                        </p>
                    </div>

                    {loading ? (
                        <div className="text-center">加载中...</div>
                    ) : (
                        <>
                            <div className="flex justify-center space-x-2 pb-8">
                                <Button
                                    key="all-categories"
                                    variant={!selectedTagId ? "default" : "outline"}
                                    size="sm"
                                    onClick={() => setSelectedTagId(null)}
                                >
                                    全部
                                </Button>
                                {tags.map((tag) => (
                                    <Button
                                        key={tag.id}
                                        variant={selectedTagId === tag.id ? "default" : "outline"}
                                        size="sm"
                                        onClick={() => setSelectedTagId(tag.id)}
                                    >
                                        {tag.name}
                                    </Button>
                                ))}
                            </div>
                            <CourseGrid courses={courses} />
                        </>
                    )}
                </Container>
            </main>
            <SiteFooter />
        </>
    );
}
