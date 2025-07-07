import logging
import os.path
from typing import List, Union

from ninja import Router

from apps.core import R, token_util, auth
from apps.course.models import Favorite, Course, Enrollment
from apps.course.schemas import CourseSchema
from apps.user.models import Banner, User, Feedback, Message, Progress, Certificate, Evaluation, Order, Invoice, VipProduct
from apps.user.schemas import (
    LoginSchema,
    RegisterSchema,
    BannerSchema,
    UserSchema,
    FeedbackSchema,
    LoginResult,
    UserInfo,
    MessageSchema,
    ProgressSchema,
    CertificateSchema,
    EvaluationSchema,
    OrderSchema,
    InvoiceSchema,
    CourseOrderSubmitSchema,
    VipOrderSubmitSchema,
)
from ninja import File, UploadedFile
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model
from django.utils import timezone

from server import settings

# Create your views here.

router = Router()
User = get_user_model()


@router.post("/login", summary="登录", response=Union[LoginResult, R])
def auth_login(request, auth: LoginSchema):
    try:
        obj = User.objects.get(username=auth.username)
        if not check_password(auth.password, obj.password):
            # 验证失败
            return R.fail("用户名或密码错误")
    except User.DoesNotExist:
        # 用户不存在，直接返回失败
        return R.fail("用户名或密码错误")

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

    # 创建新的报名记录，状态设置为"未支付"
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


@router.get("/me", summary="获取当前用户信息", response=UserInfo, **auth)
def get_current_user(request):
    user = User.objects.get(id=request.auth)
    return UserInfo(
        username=user.username,
        nickname=user.nickname,
        real_name=user.real_name,
        email=user.email,
        phone=user.phone,
        remark=user.remark,
        avatar=user.avatar.url if user.avatar else None,
        is_vip=user.is_vip,
        vip_expire_time=user.vip_expire_time,
    )


@router.get("/messages", summary="获取用户消息", response=List[MessageSchema], **auth)
def get_user_messages(request):
    return Message.objects.filter(user_id=request.auth).order_by("-created_at")


@router.get("/progress", summary="获取用户学习进度", response=List[ProgressSchema], **auth)
def get_user_progress(request):
    return Progress.objects.filter(user_id=request.auth).order_by("-last_view_time")


@router.get("/certificates", summary="获取用户证书", response=List[CertificateSchema], **auth)
def get_user_certificates(request):
    return Certificate.objects.filter(user_id=request.auth).order_by("-issue_time")


@router.get("/evaluations", summary="获取用户评价", response=List[EvaluationSchema], **auth)
def get_user_evaluations(request):
    return Evaluation.objects.filter(user_id=request.auth).order_by("-created_at")


@router.get("/orders", summary="获取用户订单", response=List[OrderSchema], **auth)
def get_user_orders(request):
    return Order.objects.filter(user_id=request.auth).order_by("-created_at")


@router.get("/invoices", summary="获取用户发票", response=List[InvoiceSchema], **auth)
def get_user_invoices(request):
    return Invoice.objects.filter(order__user_id=request.auth).order_by("-created_at")


@router.get("/feedbacks", summary="获取用户反馈", response=List[FeedbackSchema], **auth)
def get_user_feedbacks(request):
    return Feedback.objects.filter(user_id=request.auth).order_by("-id")


@router.post("/order/submit_course_payment", summary="提交支付信息", **auth)
def submit_payment(request, data: CourseOrderSubmitSchema):
    course = Course.objects.get(id=data.course_id)
    order = Order.objects.create(
        user_id=request.auth,
        course_id=data.course_id,
        status="unpaid",
        pay_type=data.pay_type,
        pay_time=None,
        order_no=f"ORDER{timezone.now().strftime('%Y%m%d%H%M%S')}{request.auth}",
        amount=course.price,
        created_at=timezone.now()
    )
    order.pay_serial_no = data.pay_serial_no
    order.save()
    return R.ok(data={
        "order_id": order.id,
        "order_no": order.order_no,
        "amount": order.amount,
        "status": order.status
    })


@router.post("/order/submit_vip_payment", summary="提交VIP支付信息", **auth)
def submit_vip_payment(request, data: VipOrderSubmitSchema):
    vip_product = VipProduct.objects.get(id=data.vip_product_id)
    order = Order.objects.create(
        user_id=request.auth,
        order_type="vip",
        status="unpaid",
        pay_type=data.pay_type,
        pay_serial_no=data.pay_serial_no,
        pay_time=None,
        order_no=f"VIP{timezone.now().strftime('%Y%m%d%H%M%S')}{request.auth}",
        amount=vip_product.price,
        created_at=timezone.now(),
        pay_remark=vip_product.name
    )
    return R.ok(data={
        "order_id": order.id,
        "order_no": order.order_no,
        "amount": order.amount,
        "status": order.status,
        "vip_type": vip_product.vip_type
    })
