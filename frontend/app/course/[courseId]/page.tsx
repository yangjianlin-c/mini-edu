"use client"

import { useEffect, useState, use } from "react"
import Link from "next/link"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import { Container } from "@/components/ui/container"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tag, Video, Unlock, Lock, PlayCircle, FolderOpen, BookOpen, Coins } from "lucide-react"
import Image from "next/image"
import { useRouter } from "next/navigation"
import { getCurrentUser } from "@/api/user"
import { getCourse, createOrderForCourse, getCourseChapters } from "@/api/course"
import { CourseDetail, User } from "@/types/course"
import { getImageUrl } from '@/api/config'; // 确保你导入了 getImageUrl 函数

export default function CoursePage({ params }) {
  const router = useRouter();
  const [course, setCourse] = useState<CourseDetail | null>(null);
  const [chapters, setChapters] = useState<any[]>([]);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const { courseId } = use(params);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 获取课程信息
        if (courseId !== undefined) { // Use the unwrapped courseId
          const courseData = await getCourse(courseId);
          console.log("course data:", courseData.data);
          setCourse({
            ...courseData.data,
            image: getImageUrl(courseData.data.image || courseData.data.thumbnail || "")
          });

          // 获取课程章节信息
          const chaptersData = await getCourseChapters(courseId);
          console.log("chapters data:", chaptersData.data);
          setChapters(chaptersData.data);
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
    if (!user) {
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
      const courseData = await getCourse(courseId);
      setCourse({
        ...courseData.data,
        image: getImageUrl(courseData.data.image || courseData.data.thumbnail || "")
      });

      // 如果是免费课程，直接跳转到第一个视频
      if (course.price === 0 && course.lessons.length > 0) {
        router.push(`/courses/${course.id}/videos/${course.lessons[0].id}`);
      }
    } catch (error) {
      toast.error("购买失败，请稍后重试");
    }
  };

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
      <main className="flex-1 bg-background">
        <Container className="py-8 md:py-12">
          <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-10">
            {/* 左侧：课程信息 */}
            <div className="space-y-6">
              <div className="overflow-hidden rounded-xl shadow-md border">
                <Image
                  src={course.image || `/${course.id}.png`}
                  alt={course.title}
                  width={600}
                  height={400}
                  className="w-full h-auto object-cover"
                />
              </div>

              <div className="space-y-3">
                <h1 className="text-2xl font-bold flex items-center gap-2 mb-2">
                  <BookOpen className="w-6 h-6 text-primary" />
                  {course.title}
                </h1>

                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <span className="text-lg font-semibold">¥</span>
                  <span className="text-lg font-semibold text-primary">{course.price}</span>
                </div>

                {course.tags?.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {course.tags.map((tag) => (
                      <Badge key={tag.id} variant="outline" className="flex items-center gap-1">
                        <Tag className="w-3 h-3" />
                        {tag.name}
                      </Badge>
                    ))}
                  </div>
                )}



                <p className="text-muted-foreground text-sm leading-relaxed">
                  {course.description}
                </p>

                <Button
                  className="w-full flex items-center justify-center gap-2"
                  onClick={handlePurchase}
                  disabled={hasPurchased}
                  variant={hasPurchased ? "outline" : "default"}
                >
                  {hasPurchased ? (
                    <>
                      <Unlock className="h-4 w-4" />
                      已购买
                    </>
                  ) : isFreeCourse ? (
                    <>
                      <Unlock className="h-4 w-4" />
                      免费加入
                    </>
                  ) : (
                    <>
                      <Lock className="h-4 w-4" />
                      立即购买
                    </>
                  )}
                </Button>
              </div>
            </div>

            {/* 右侧：章节与视频列表 */}
            <div className="md:col-span-2 space-y-6">
              <h2 className="text-xl font-semibold"> 课程内容</h2>
              {(chapters || []).map((chapter) => (

                <Card key={chapter.id} className="border shadow-sm">
                  <CardHeader className="pb-2 flex flex-col gap-1">
                    <div className="flex items-center gap-2">
                      <FolderOpen className="w-5 h-5 text-muted-foreground" />
                      <h3 className="text-lg font-medium">{chapter.title}</h3>
                    </div>
                    {chapter.description && (
                      <CardDescription>{chapter.description}</CardDescription>
                    )}
                  </CardHeader>
                  <CardContent className="pt-0 space-y-2">
                    {(chapter.videos || []).map((video) => (
                      <Link
                        key={video.id}
                        href={`/courses/${course.id}/videos/${video.id}`}
                        className="block"
                      >
                        <Button
                          variant="outline"
                          className="w-full flex justify-start items-center gap-2"
                        >
                          <PlayCircle className="w-4 h-4 text-primary" />
                          <span className="truncate">{video.title}</span>
                        </Button>
                      </Link>
                    ))}
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </Container>
      </main>
      <SiteFooter />
    </>


  );
}
