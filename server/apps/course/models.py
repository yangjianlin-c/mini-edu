from django.db import models
from mdeditor.fields import MDTextField
from django.utils.timezone import now
from apps.user.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签管理"


default_tell = """#### 课程须知
如果有问题及时反馈  
#### 你能学到什么
Django Ninja & React 前后端的使用
"""


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name="名称")
    description = models.CharField(max_length=255, verbose_name="简介")
    level = models.IntegerField(
        choices=((3, "初级"), (2, "中级"), (1, "高级")), verbose_name="难度"
    )
    study_number = models.IntegerField(verbose_name="学习人数", default=0)
    favorite_number = models.IntegerField(default=0, verbose_name="收藏数")
    tell = MDTextField(verbose_name="需要告知的内容", default=default_tell)
    image = models.ImageField(upload_to="courses/", verbose_name="图片")
    is_feature = models.BooleanField(default=False, verbose_name="精选课程")
    price = models.IntegerField(verbose_name="课程价格（元）", default=0)
    tags = models.ManyToManyField(Tag, related_name="courses", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = "01-课程管理"


class Chapter(models.Model):
    title = models.CharField(max_length=50, verbose_name="名称")
    description = models.CharField(max_length=200, verbose_name="简介")
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="所属课程", null=True
    )
    sort_number = models.IntegerField(default=999, verbose_name="序号")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = "02-章节管理"


Video_Source = (
    ("bili", "Bilibili"),
    ("qiniu", "Qiniu Cloud"),
    ("local", "Local"),
)


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    chapter = models.ForeignKey(
        Chapter, verbose_name="所属章节", on_delete=models.SET_NULL, null=True
    )
    free_preview = models.BooleanField(default=False)
    video_source = models.CharField(max_length=20, choices=Video_Source)
    video_url = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    file = models.FileField(upload_to="courses/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "课时"
        verbose_name_plural = "03-课时管理"


STATUS_CHOICES = (
    ("unpaid", "未支付"),
    ("paid", "已支付"),
    ("cancelled", "已取消"),
)


class Enrollment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="用户", null=True
    )
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="课程", null=True
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="unpaid")
    create_time = models.DateTimeField(verbose_name="创建时间", default=now)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __str__(self):
        return f"{self.user.username} 加入了 {self.course.title} 课程"

    class Meta:
        verbose_name = "订购课程"
        verbose_name_plural = "04-订购课程管理"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="用户", null=True
    )
    content = models.TextField(verbose_name="评论内容")
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="课程", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论管理"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="课程",
        related_name="favorites",
    )

    def __str__(self):
        return f"用户 {self.user.username} 收藏了课程 {self.course.title}"

    class Meta:
        verbose_name = "收藏课程"
        verbose_name_plural = "收藏课程管理"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.course.favorite_number = self.course.favorites.count()
        self.course.save()
