from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(
        max_length=30, verbose_name="昵称", null=True, blank=True
    )
    avatar = models.ImageField(
        upload_to="avatars/", verbose_name="头像", default="avatars/default.jpg"
    )
    register_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    last_active_time = models.DateTimeField(auto_now=True, verbose_name="最新活动时间")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户管理"


class Banner(models.Model):
    image = models.ImageField(upload_to="banners/", verbose_name="轮播图")
    to_id = models.IntegerField(null=True, blank=True, verbose_name="跳转ID")
    sort_number = models.IntegerField(default=999, verbose_name="序号")

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = "轮播图管理"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.TextField(verbose_name="内容")
    phone = models.CharField(
        max_length=11, verbose_name="联系电话", null=True, blank=True
    )
    status = models.IntegerField(
        choices=((1, "已回复"), (2, "待回复")), verbose_name="是否回复", default=2
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "反馈"
        verbose_name_plural = "反馈管理"
