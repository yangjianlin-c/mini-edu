from typing import List

from ninja import ModelSchema, Schema, Field

from apps.course.models import Course, Chapter, Comment, Lesson, Enrollment, Tag
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
        fields = "__all__"


class ChapterSchema(ModelSchema):
    Lessons: List[LessonSchema] = None

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
