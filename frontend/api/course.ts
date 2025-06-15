import {host,getImageUrl} from './config'
import api from "./req";
import { Course } from "../types/course";


// 获取课程tag列表
export function listTags() {
  return api({ method: "GET", url: "course/tags" });
}


// 获取所有课程
export function listCourses(): Promise<Course[]> {
  return api({
    method: "GET",
    url: "/course/all",
  }).then((res) => {
    if (res.data) {
      return res.data.map((course: Course) => ({
        ...course,
        image: getImageUrl(course.image),
      }));
    }
    return [];
  });
}

// 获取单个课程详情
export function getCourse(course_id: number): Promise<{ data: CourseDetail }> {
  return api({ method: "GET", url: `course/${course_id}` }).then((response) => {
    if (response.data) {
      // 统一使用 image 字段名
      response.data.image = getImageUrl(response.data.image || response.data.thumbnail || "")
    }
    return response
  })
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

