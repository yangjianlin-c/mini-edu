"use client"

import { useEffect, useState } from "react"
import * as React from 'react'
import Link from "next/link"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import { Container } from "@/components/ui/container"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tag, Video, Unlock, Lock } from "lucide-react"
import Image from "next/image"
import { useRouter } from "next/navigation"
import { getCurrentUser } from "@/api/user"
import { getCourse, createOrderForCourse } from "@/api/course"
import { CourseDetail } from "@/types/course"

export default function CoursePage({ params }) {
  const router = useRouter()
  const [course, setCourse] = useState<CourseDetail | null>(null)
  const [currentUser, setCurrentUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const { courseId } = React.use(params)

  useEffect(() => {
    const fetchData = async () => {
      try {

        // 获取课程信息
        if (courseId !== null) { // Use the unwrapped courseId
          const data = await getCourse(courseId);
          console.log("course data:", data.data);
          setCourse(data.data);
        }
      } catch (error) {
        console.error("获取数据失败:", error);
        toast.error("获取数据失败");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [courseId]);

  const handlePurchase = async () => {
    const user = await getCurrentUser();
    setCurrentUser(user);
    if (!currentUser) {
      router.push('/auth/login');
      toast.info("请先登录后再购买课程");
      return;
    }

    if (!course) return;

    // 检查是否已购买
    const hasPurchased = course.enrolled_users?.some(user => user.id === currentUser.id);
    if (hasPurchased) {
      toast.info("您已购买此课程，可直接观看");
      return;
    }

    try {
      // 调用购买接口
      await createOrderForCourse(course.id);
      toast.success("课程购买成功！");

      // 刷新课程数据
      const data = await getCourse(course.id);
      setCourse(data);

      // 如果是免费课程，直接跳转到第一个视频
      if (course.price === 0 && course.lessons.length > 0) {
        router.push(`/courses/${course.id}/videos/${course.lessons[0].id}`);
      }
    } catch (error) {
      toast.error("购买失败，请稍后重试");
    }
  }

  if (loading) {
    return <div>加载中...</div>;
  }

  if (!course) {
    return <div>课程不存在</div>;
  }


  const hasPurchased = currentUser && course.enrolled_users?.some(user => user.id === currentUser.id);
  const isFreeCourse = course?.price === 0;

  return (
    <>
      <SiteHeader />
      <main className="flex-1">
        <Container className="py-8 md:py-12">
          <div className="grid gap-8 md:grid-cols-[1fr_2fr]">
            <div className="space-y-4">
              <h1 className="text-3xl font-bold">{course.title}</h1>
              <div className="overflow-hidden rounded-lg">
                <Image
                  src={course.image || `/${course.id}.png`}
                  alt={course.title}
                  width={800}
                  height={400}
                  className="w-full h-auto object-cover"
                />
              </div>
              <div className="flex items-center gap-2 text-muted-foreground">
                <Tag className="h-4 w-4" />
                <span>￥{course.price}</span>
              </div>
              {course.tags && course.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {course.tags.map((tag) => (
                    <span key={tag.id} className="text-xs bg-secondary text-secondary-foreground px-2 py-1 rounded">
                      {tag.name}
                    </span>
                  ))}
                </div>
              )}
              <p className="text-lg">{course.description}</p>
              <Button
                className="w-full flex items-center justify-center gap-2"
                onClick={handlePurchase}
                disabled={hasPurchased}
                variant={(hasPurchased) ? "outline" : "default"}
              >
                {hasPurchased ? (
                  <>
                    <Unlock className="h-4 w-4" />
                    <span>已购买</span>
                  </>
                ) : isFreeCourse ? (
                  <>
                    <Unlock className="h-4 w-4" />
                    <span>免费加入</span>
                  </>
                ) : (
                  <>
                    <Lock className="h-4 w-4" />
                    <span>立即购买</span>
                  </>
                )}
              </Button>
            </div>


          </div>
        </Container>
      </main>
      <SiteFooter />
    </>
  )
}