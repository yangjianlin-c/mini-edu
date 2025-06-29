from typing import List

from ninja import Router

from apps.core import auth, R
from apps.course.models import Course, Chapter, Comment, Lesson, Tag, Favorite
from apps.course.schemas import (
    CourseListSchema,
    CourseSchema,
    ChapterSchema,
    CommentSchema,
    CommentCreate,
    LessonSchema,
    TagSchema,
)
from django.core.paginator import Paginator

# Create your views here.

router = Router()


@router.get("/feature", summary="推荐课程", response=List[CourseListSchema])
def get_feature_courses(request):
    courses = Course.objects.filter(is_feature=True).order_by("-created_at")[:3]
    return courses


@router.get("/list", summary="课程列表", response=List[CourseListSchema])
def get_course_list(request, title: str = None, tag_id: int = None):
    filters = {}
    if title:
        filters = {"title__icontains": title}
    if tag_id:
        filters["tags__id"] = tag_id
    courses = Course.objects.filter(**filters)
    paginator = Paginator(courses, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj


@router.get("/{id}", summary="课程详情", response=CourseSchema)
def get_course_by_id(request, id: int):
    return Course.objects.get(id=id)


@router.get("/chapter/list", summary="章节列表", response=List[ChapterSchema])
def get_chapters_by_course_id(request, course_id: int):
    chapters = Chapter.objects.filter(course_id=course_id).all()
    for chapter in chapters:
        setattr(chapter, "lessons", chapter.lesson_set.all())
    return chapters


@router.get("/lesson/", summary="视频详情", response=LessonSchema)
def get_lesson_by_id(request, id: int):
    return Lesson.objects.get(id=id)


@router.get("/comment/list", summary="评论列表", response=List[CommentSchema])
def get_comments_by_course_id(request, course_id: int):
    objs = Comment.objects.filter(course_id=course_id).all()
    for obj in objs:
        setattr(obj, "user", obj.user)
    return objs


@router.post("/comment/add", summary="添加评论", **auth)
def add_comment(request, data: CommentCreate):
    Comment.objects.create(**data.dict(), user_id=request.auth)
    return R.ok()


# Tag
@router.get("/tag/list", summary="标签列表", response=List[TagSchema])
def get_tags_all(request):
    return Tag.objects.all()


@router.post("/favorite/toggle", summary="切换课程收藏")
def toggle_favorite(request, course_id: int):
    user = request.user  # 获取当前登录用户
    Favorite.toggle_favorite(course_id, user)
    return R.ok(msg="课程收藏状态切换成功")
