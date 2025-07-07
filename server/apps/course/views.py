from typing import List

from ninja import Router

from apps.core import auth, R
from apps.course.models import Course, Comment, Lesson, Tag, Favorite, Enrollment
from apps.course.schemas import (
    CourseListSchema,
    CourseSchema,
    CommentSchema,
    CommentCreate,
    LessonSchema,
    TagSchema,
    CommentReplySchema,
    CommentLikeSchema,
    CommentDeleteSchema,
    ProgressReportSchema,
    EnrollmentCreateSchema,
    CertificateGetSchema,
    CourseListQuerySchema,
)
from django.core.paginator import Paginator
from django.db.models import Q
from apps.user.models import Progress, Certificate

# Create your views here.

router = Router()


@router.get("/feature", summary="推荐课程", response=List[CourseListSchema])
def get_feature_courses(request):
    courses = Course.objects.filter(is_feature=True).order_by("-created_at")[:3]
    return courses


@router.get("/list", summary="课程列表", response=List[CourseListSchema])
def get_course_list(request, title: str = None, tag_ids: str = None, page: int = 1, page_size: int = 10):
    filters = Q()
    if title:
        filters &= Q(title__icontains=title)
    if tag_ids:
        tag_id_list = [int(i) for i in tag_ids.split(",") if i.isdigit()]
        if tag_id_list:
            filters &= Q(tags__id__in=tag_id_list)
    courses = Course.objects.filter(filters).distinct()
    paginator = Paginator(courses, page_size)
    page_obj = paginator.get_page(page)
    return page_obj


@router.get("/{id}", summary="课程详情", response=CourseSchema)
def get_course_by_id(request, id: int):
    return Course.objects.get(id=id)


@router.get("/lesson/list", summary="课时列表", response=List[LessonSchema])
def get_lessons_by_course_id(request, course_id: int):
    lessons = Lesson.objects.filter(course_id=course_id).order_by("sort_number", "id")
    return lessons


@router.get("/lesson/", summary="课时详情", response=LessonSchema)
def get_lesson_by_id(request, id: int):
    return Lesson.objects.get(id=id)


@router.get("/comment/list", summary="评论列表", response=List[CommentSchema])
def get_comments_by_course_id(request, course_id: int, page: int = 1, page_size: int = 10):
    objs = Comment.objects.filter(course_id=course_id, is_deleted=False).order_by("-created_at")
    paginator = Paginator(objs, page_size)
    page_obj = paginator.get_page(page)
    for obj in page_obj:
        setattr(obj, "user", obj.user)
    return page_obj


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


@router.get("/favorite/list", summary="获取用户收藏课程", response=List[CourseListSchema])
def get_favorite_courses(request):
    user_id = request.auth
    favorites = Favorite.objects.filter(user_id=user_id)
    return [fav.course for fav in favorites]


@router.post("/comment/reply", summary="回复评论")
def reply_comment(request, data: CommentReplySchema):
    Comment.objects.create(
        content=data.content,
        parent_id=data.parent_id,
        course_id=data.course_id,
        user_id=request.auth
    )
    return R.ok()


@router.post("/comment/like", summary="点赞评论")
def like_comment(request, data: CommentLikeSchema):
    from apps.course.models import Like
    Like.objects.get_or_create(user_id=request.auth, comment_id=data.comment_id)
    return R.ok()


@router.post("/comment/delete", summary="删除评论")
def delete_comment(request, data: CommentDeleteSchema):
    Comment.objects.filter(id=data.comment_id, user_id=request.auth).update(is_deleted=True)
    return R.ok()


@router.post("/progress/report", summary="上报学习进度")
def report_progress(request, data: ProgressReportSchema):
    obj, _ = Progress.objects.update_or_create(
        user_id=request.auth,
        course_id=data.course_id,
        lesson_id=data.lesson_id,
        defaults={"progress": data.progress}
    )
    return R.ok()


@router.get("/progress/get", summary="获取课程学习进度")
def get_progress(request, course_id: int):
    objs = Progress.objects.filter(user_id=request.auth, course_id=course_id)
    return [
        {"lesson_id": obj.lesson_id, "progress": obj.progress, "last_view_time": obj.last_view_time}
        for obj in objs
    ]


@router.post("/enroll", summary="报名/购买课程")
def enroll_course(request, data: EnrollmentCreateSchema):
    obj, created = Enrollment.objects.get_or_create(
        user_id=request.auth,
        course_id=data.course_id,
        defaults={"status": "unpaid"}
    )
    return R.ok(data={"enrollment_id": obj.id, "status": obj.status})


@router.get("/certificate/get", summary="获取课程证书")
def get_certificate(request, course_id: int):
    cert = Certificate.objects.filter(user_id=request.auth, course_id=course_id).first()
    if cert:
        return {"issue_time": cert.issue_time, "download_url": cert.download_url}
    return R.fail("未获得证书")
