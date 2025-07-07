from django.contrib import admin
from .models import User, Banner, Feedback, VipProduct


# 使用Django默认的admin功能
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "nickname", "last_active_time")
    search_fields = ("username", "nickname")
    list_filter = ("register_time", "last_active_time")

    def save_model(self, request, obj, form, change):
        # 如果设置了VIP且有VIP产品，则自动计算到期时间
        if obj.is_vip and obj.vip_product:
            obj.activate_or_renew_vip(obj.vip_product)
        else:
            super().save_model(request, obj, form, change)


admin.site.register(Banner)
admin.site.register(Feedback)

admin.site.register(VipProduct)

admin.site.site_header = "在线教育后台"
admin.site.site_index = "在线教育"
