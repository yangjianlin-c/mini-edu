
// 在 types/course.ts 文件中定义 Course 接口

export interface CourseTag {
  id: number;
  name: string;
}

export interface Course {
  id: number;
  title: string;
  description: string;
  level: number;
  study_number: number;
  like_number: number;
  tell: string;
  image: string;
  sort_number: number;
  price: number;
  created_at: string;
  updated_at: string;
  tags: CourseTag[];
}



export interface CourseDetail {
  id: number
  title: string
  description: string
  price: number
  image: string
  tags: CourseTag[]
  lessons: Lesson[]
  enrolled_users: any[]
}


export type Lesson = {
  id: number
  title: string
  video_source: string
  video_url: string | null
  content: string
  free_preview: boolean
  created_at: string | null
  updated_at: string | null
  course_id: number
}



