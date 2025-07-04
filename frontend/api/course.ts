// 在 frontend/api/course.ts 文件中

import { host, getImageUrl } from './config';
import api from "./req";
import { Course } from "../types/course"; // 使用新的接口名称

// 获取课程tag列表
export function listTags() {
  return api({ method: "GET", url: "course/tag/list" })
    .then((res) => res.data || []);
}

// 获取所有课程
export function listCourses(name?: string, tag_id?: number): Promise<Course[]> {
  const params = new URLSearchParams({
    ...(name && { name }),
    ...(tag_id !== undefined && { tag_id: tag_id.toString() }),
  });

  const url = `/course/all${params.toString() ? `?${params.toString()}` : ""}`;

  return api({ method: "GET", url }).then((res) => res.data || []);
}


// 获取单个课程详情
export function getCourse(courseId: number): Promise<{ data: Course }> {
  return api({ method: "GET", url: `course/${courseId}` });
}

// 获取课程章节列表
export function getCourseChapters(courseId: number): Promise<{ data: any[] }> {
  return api({ method: "GET", url: `course/chapter/list`, params: { course_id: courseId } });
}

// 获取课程下的课时
export function listLessons(course_id: number) {
  return api({ method: "GET", url: `course/${course_id}/lessons` });
}

// 获取单个课时详情
export function getLesson(lesson_id: number) {
  return api({ method: "GET", url: `course/lesson/${lesson_id}` });
}

// 为课程创建订单
export function createOrderForCourse(course_id: number, note?: string) {
  return api({
    method: "POST",
    url: "order/create",
    data: {
      course_id,
      note
    }
  });
}
