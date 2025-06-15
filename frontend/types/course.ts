// types/course.ts

export interface CourseSummary {
  id: number
  title: string
  description: string
  level: number
  study_number: number
  like_number: number
  tell: string
  image: string
  sort_number: number
  price: number
  created_at: string
  updated_at: string
  tags: number[]
}

export interface CourseDetail {
  id: number
  title: string
  description: string
  price: number
  image: string
  tags: Tag[]
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

export interface Tag {
  id: number
  name: string
}
