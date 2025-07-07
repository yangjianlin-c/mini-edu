from django.contrib import admin

from .models import Course, Lesson, Comment, Favorite, Enrollment, Tag

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "study_number", "level", "is_feature")
    search_fields = ("title",)
    list_filter = ("level", "is_feature")

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "sort_number", "free_preview", "video_source")
    search_fields = ("title", "course__title")
    list_filter = ("course",)

admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Enrollment)
admin.site.register(Tag)
