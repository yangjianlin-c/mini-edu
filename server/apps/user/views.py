import logging
import os.path
from typing import List, Union

from ninja import Router

from apps.core import R, token_util, auth
from apps.course.models import Favorite, Course, Enrollment
from apps.course.schemas import CourseSchema
from apps.user.models import Banner, User, Feedback
from apps.user.schemas import (
    LoginSchema,
    RegisterSchema,
    BannerSchema,
    UserSchema,
    FeedbackSchema,
    LoginResult,
)
from ninja import File, UploadedFile
from django.contrib.auth.hashers import make_password, check_password

from server import settings

# Create your views here.

router = Router()


@router.post("/login", summary="登录", response=Union[LoginResult, R])
def auth_login(request, auth: LoginSchema):
    try:
        obj = User.objects.get(username=auth.username)
        if not check_password(auth.password, obj.password):
            # 验证失败
            return R.fail("用户名或密码错误")
    except User.DoesNotExist:
        # 用户不存在
        password = make_password(auth.password)  # 对密码进行哈希处理
        obj = User.objects.create(username=auth.username, password=password)

    # 生成token
    token = token_util.build(obj.id)
    return {"token": token, "user": obj}


@router.post("/register", summary="注册", response=Union[LoginResult, R])
def auth_register(request, register_data: RegisterSchema):
    try:
        # 检查用户名是否已存在
        if User.objects.filter(username=register_data.username).exists():
            return R.fail("用户名已存在")

        # 创建新用户
        password = make_password(register_data.password)  # 对密码进行哈希处理
        user = User.objects.create(
            username=register_data.username,
            email=register_data.email,
            password=password,
        )

        # 生成token
        token = token_util.build(user.id)
        return {"token": token, "user": user}

    except Exception as e:
        logging.error(f"注册失败: {e}")
        return R.fail("注册失败")


@router.post("/logout", summary="退出")
def auth_logout(request):
    request.session.clear()
    return R.ok()


@router.post("/avatar", summary="上传头像", **auth)
def auth_avatar(request, avatar: UploadedFile = File(...)):
    root = settings.MEDIA_ROOT / "avatars"
    if not os.path.isdir(root):
        os.mkdir(root)
    with open(root / avatar.name, "wb") as w:
        w.write(avatar.read())
    user = User.objects.get(id=request.auth)
    user.avatar = f"avatars/{avatar.name}"
    user.save()
    return R.ok(data={"url": user.avatar.url})


@router.patch("/profile", summary="修改信息", **auth)
def auth_profile(request, data: UserSchema):
    if obj := data.dict(exclude_unset=True):
        if "password" in obj:
            obj["password"] = make_password(obj["password"])
        User.objects.filter(pk=request.auth).update(**obj)
        return R.ok()
    return R.fail("无效修改")


###


@router.get("/banner", summary="轮播图", response=List[BannerSchema])
def get_banners(request):
    return Banner.objects.all().order_by("-sort_number")


@router.get(
    "/favorite", summary="根据操作类型获取课程", response=List[CourseSchema], **auth
)
def get_courses_by_favorite(request):
    objs = Favorite.objects.filter(user_id=request.auth)
    return [obj.course for obj in objs]


@router.post("/favorite", summary="收藏课程", **auth)
def add_user_favorite(request, course_id: int):
    kwargs = dict(user_id=request.auth, course_id=course_id)
    course = Course.objects.filter(id=course_id).first()
    if not course:
        return R.fail("课程不存在")
    try:
        obj = Favorite.objects.get(**kwargs)
        obj.delete()
        logging.info(f"{obj.user_id} 取消收藏课程 {course_id}")
        return R.ok(msg="已取消收藏")
    except Favorite.DoesNotExist:
        Favorite.objects.create(**kwargs)
        logging.info(f"{request.auth} 收藏课程 {course_id}")
        return R.ok(msg="收藏成功")


@router.get(
    "/enrollment", summary="获取用户报名的课程", response=List[CourseSchema], **auth
)
def get_user_enrollment(request):
    objs = Enrollment.objects.filter(user_id=request.auth)
    return [obj.course for obj in objs]


@router.post("/enrollment", summary="报名课程", **auth)
def add_user_enrollment(request, course_id: int):
    user_id = request.auth.get("user_id")

    course = Course.objects.filter(id=course_id).first()
    if not course:
        return R.fail("课程不存在")

    # 检查用户是否已经报名了该课程
    enrollment = Enrollment.objects.filter(user_id=user_id, course_id=course_id).first()
    if enrollment:
        return R.fail("您已经报名了该课程")

    # 创建新的报名记录，状态设置为“未支付”
    enrollment = Enrollment.objects.create(
        user_id=user_id, course_id=course_id, status="unpaid"
    )
    logging.info(f"{user_id} 报名了课程 {course_id}，状态为未支付")
    return R.ok(
        msg="报名成功",
        data={"course_id": enrollment.course_id, "status": enrollment.status},
    )


@router.post("/feedback", summary="反馈留言", **auth)
def add_feedback(request, data: FeedbackSchema):
    Feedback.objects.create(user_id=request.auth, **data.dict())
    return R.ok()
