from typing import List

from ninja import ModelSchema, Schema, Field

from apps.course.models import Course, Chapter, Comment, Video, Enrollment, Tag
from apps.user.schemas import UserInfo


class TagSchema(ModelSchema):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class CourseSchema(ModelSchema):
    tags: List[TagSchema]

    class Meta:
        model = Course
        fields = "__all__"


class VideoSchema(ModelSchema):
    class Meta:
        model = Video
        fields = "__all__"


class ChapterSchema(ModelSchema):
    videos: List[VideoSchema] = None

    class Meta:
        model = Chapter
        fields = "__all__"


class CommentSchema(ModelSchema):
    user: UserInfo = None

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
