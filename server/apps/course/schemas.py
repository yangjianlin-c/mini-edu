from typing import List, Optional

from ninja import ModelSchema, Schema, Field

from apps.course.models import Course, Comment, Lesson, Enrollment, Tag
from apps.user.schemas import UserInfo


class TagSchema(ModelSchema):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class CourseListSchema(ModelSchema):
    tags: List[TagSchema]

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "level",
            "study_number",
            "favorite_number",
            "tags",
            "image",
            "price",
        ]


class CourseSchema(ModelSchema):
    tags: List[TagSchema]

    class Meta:
        model = Course
        fields = "__all__"


class LessonSchema(ModelSchema):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "course",
            "sort_number",
            "free_preview",
            "video_source",
            "video_url",
            "content",
            "file",
            "created_at",
            "update_time"
        ]


class CommentSchema(ModelSchema):
    user: Optional[UserInfo] = None

    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreate(Schema):
    content: str = Field(..., description="评论内容")
    course_id: int = Field(..., description="课程ID")


class EnrollmentSchema(Schema):
    class Meta:
        model = Enrollment
        fields = "__all__"


class CommentReplySchema(Schema):
    content: str = Field(..., description="回复内容")
    parent_id: int = Field(..., description="父评论ID")
    course_id: int = Field(..., description="课程ID")


class CommentLikeSchema(Schema):
    comment_id: int = Field(..., description="评论ID")


class CommentDeleteSchema(Schema):
    comment_id: int = Field(..., description="评论ID")


class ProgressReportSchema(Schema):
    course_id: int = Field(..., description="课程ID")
    lesson_id: int = Field(..., description="课时ID")
    progress: float = Field(..., description="进度百分比")


class EnrollmentCreateSchema(Schema):
    course_id: int = Field(..., description="课程ID")


class CertificateGetSchema(Schema):
    course_id: int = Field(..., description="课程ID")


class CourseListQuerySchema(Schema):
    title: Optional[str] = Field(None, description="课程标题关键字")
    tag_ids: Optional[str] = Field(None, description="标签ID列表,逗号分隔")
    page: Optional[int] = Field(1, description="页码")
    page_size: Optional[int] = Field(10, description="每页数量")
