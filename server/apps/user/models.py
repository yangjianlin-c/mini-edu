from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
import datetime


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, verbose_name="账号")
    password = models.CharField(max_length=50, verbose_name="密码")
    nickname = models.CharField(
        max_length=30, verbose_name="昵称", null=True, blank=True
    )
    real_name = models.CharField(
        max_length=30, verbose_name="真实姓名", null=True, blank=True
    )
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    phone = models.CharField(
        max_length=20, verbose_name="手机号", null=True, blank=True
    )
    remark = models.CharField(
        max_length=255, verbose_name="备注", null=True, blank=True
    )
    avatar = models.ImageField(
        upload_to="avatars/", verbose_name="头像", default="avatars/default.jpg"
    )
    register_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    last_active_time = models.DateTimeField(auto_now=True, verbose_name="最新活动时间")
    is_vip = models.BooleanField(default=False, verbose_name="是否VIP")
    vip_expire_time = models.DateTimeField(
        null=True, blank=True, verbose_name="VIP到期时间"
    )
    vip_product = models.ForeignKey(
        "VipProduct",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="VIP产品",
    )

    def __str__(self):
        return self.username

    def activate_or_renew_vip(self, vip_product):
        self.is_vip = True
        self.vip_product = vip_product
        now = timezone.now()
        if vip_product.vip_type == "year":
            if (
                self.vip_expire_time
                and isinstance(self.vip_expire_time, datetime.datetime)
                and self.vip_expire_time > now
            ):
                self.vip_expire_time = self.vip_expire_time + timedelta(
                    days=vip_product.duration_days
                )
            else:
                self.vip_expire_time = now + timedelta(days=vip_product.duration_days)
        elif vip_product.vip_type == "forever":
            self.vip_expire_time = None
        self.save()

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


class Message(models.Model):
    MESSAGE_TYPE = (
        ("system", "系统"),
        ("order", "订单"),
        ("course", "课程"),
        ("feedback", "反馈"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.TextField(verbose_name="消息内容")
    type = models.CharField(
        max_length=20, choices=MESSAGE_TYPE, verbose_name="消息类型"
    )
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = "用户消息管理"


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(
        "course.Course", on_delete=models.CASCADE, verbose_name="课程"
    )
    lesson = models.ForeignKey(
        "course.Lesson",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="课时",
    )
    progress = models.FloatField(default=0, verbose_name="进度(百分比)")
    last_view_time = models.DateTimeField(auto_now=True, verbose_name="最近学习时间")

    class Meta:
        verbose_name = "学习进度"
        verbose_name_plural = "学习进度管理"


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(
        "course.Course", on_delete=models.CASCADE, verbose_name="课程"
    )
    issue_time = models.DateTimeField(auto_now_add=True, verbose_name="发放时间")
    download_url = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="证书下载地址"
    )

    class Meta:
        verbose_name = "证书"
        verbose_name_plural = "证书管理"


class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(
        "course.Course", on_delete=models.CASCADE, verbose_name="课程"
    )
    score = models.IntegerField(default=5, verbose_name="评分")
    content = models.TextField(verbose_name="评价内容", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评价时间")

    class Meta:
        verbose_name = "评价"
        verbose_name_plural = "评价管理"


class Order(models.Model):
    ORDER_TYPE = (
        ("course", "课程订单"),
        ("vip", "VIP订单"),
    )
    ORDER_STATUS = (
        ("unpaid", "未支付"),
        ("paid", "已支付"),
        ("cancelled", "已取消"),
    )
    PAY_TYPE = (
        ("wechat", "微信"),
        ("alipay", "支付宝"),
        ("other", "其他"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    order_type = models.CharField(
        max_length=10, choices=ORDER_TYPE, default="course", verbose_name="订单类型"
    )
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="课程",
    )
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS, default="unpaid", verbose_name="订单状态"
    )
    pay_type = models.CharField(
        max_length=20, choices=PAY_TYPE, default="qrcode", verbose_name="支付方式"
    )
    pay_serial_no = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="支付流水号"
    )
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    order_no = models.CharField(max_length=64, unique=True, verbose_name="订单号")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    pay_remark = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="支付备注"
    )

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单管理"


class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单")
    invoice_no = models.CharField(max_length=64, unique=True, verbose_name="发票号")
    status = models.CharField(max_length=20, default="pending", verbose_name="发票状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "发票"
        verbose_name_plural = "发票管理"


class VipProduct(models.Model):
    VIP_TYPE = (
        ("year", "包年VIP"),
        ("forever", "永久VIP"),
    )
    vip_type = models.CharField(
        max_length=10, choices=VIP_TYPE, default="year", verbose_name="VIP类型"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    duration_days = models.IntegerField(
        null=True, blank=True, verbose_name="有效天数"
    )  # 永久VIP可为null

    def __str__(self):
        return self.vip_type

    class Meta:
        verbose_name = "VIP产品"
        verbose_name_plural = "VIP产品管理"
