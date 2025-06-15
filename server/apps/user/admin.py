from django.contrib import admin
from .models import User, Banner, Feedback


# 使用Django默认的admin功能
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "nickname", "last_active_time")
    search_fields = ("username", "nickname")
    list_filter = ("register_time", "last_active_time")


admin.site.register(Banner)
admin.site.register(Feedback)

admin.site.site_header = "在线教育后台"
admin.site.site_index = "在线教育"
