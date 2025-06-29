from django.contrib import admin

from .models import Course, Chapter, Lesson, Comment, Favorite, Enrollment, Tag


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 0


# 内联
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "level",
        "price",
        "study_number",
        "favorite_number",
        "is_feature",
    )
    search_fields = ("title",)
    readonly_fields = ("study_number", "favorite_number")


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "course", "sort_number")
    search_fields = ("title",)
    inlines = [LessonInline]
    list_filter = ("course",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "chapter",
    )
    search_fields = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "course",
        "content",
    )
    search_fields = (
        "user__username",
        "course__name",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "course",
        "status",
    )
    list_editable = ("status",)
    search_fields = (
        "user__username",
        "course__name",
    )
    list_filter = ("status",)
    readonly_fields = ("create_time", "update_time")


# admin.site.register(Like)
admin.site.register(Tag)


admin.site.register(Favorite)
