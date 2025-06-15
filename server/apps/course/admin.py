from django.contrib import admin

from .models import Course, Chapter, Video, Comment, Like, Enrollment, Tag


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 0


# 内联
class VideoInline(admin.StackedInline):
    model = Video
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
        "sort_number",
    )
    search_fields = ("title",)
    readonly_fields = ("study_number", "like_number")


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "course", "sort_number")
    search_fields = ("title",)
    inlines = [VideoInline]
    list_filter = ("course",)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
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


admin.site.register(Like)


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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)

    def __str__(self):
        return self.name
