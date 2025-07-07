from enum import Enum
from typing import Optional

from ninja import Schema, Field, ModelSchema

from apps.user.models import Banner, User, Message, Progress, Certificate, Evaluation, Order, Invoice


class LoginSchema(Schema):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class RegisterSchema(Schema):
    username: str = Field(..., description="用户名", example="user")
    email: str = Field(..., description="邮箱", example="user@mekesim.com")
    password: str = Field(..., description="密码", example="password")


class UserSchema(Schema):
    password: Optional[str] = Field(None, description="密码")
    nickname: Optional[str] = Field(None, description="昵称")
    real_name: Optional[str] = Field(None, description="真实姓名")
    email: Optional[str] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="手机号")
    remark: Optional[str] = Field(None, description="备注")
    avatar: Optional[str] = Field(None, description="头像 url")
    is_vip: Optional[bool] = Field(None, description="是否VIP")
    vip_expire_time: Optional[str] = Field(None, description="VIP到期时间")


class UserInfo(Schema):
    username: Optional[str] = Field(None, description="账号")
    nickname: Optional[str] = Field(None, description="昵称")
    real_name: Optional[str] = Field(None, description="真实姓名")
    email: Optional[str] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="手机号")
    remark: Optional[str] = Field(None, description="备注")
    avatar: Optional[str] = Field(None, description="头像 url")
    is_vip: Optional[bool] = Field(None, description="是否VIP")
    vip_expire_time: Optional[str] = Field(None, description="VIP到期时间")


class LoginResult(Schema):
    token: str
    user: UserInfo


class BannerSchema(ModelSchema):
    class Meta:
        model = Banner
        fields = "__all__"


class FeedbackSchema(Schema):
    content: str = Field(..., description="内容")
    phone: str = Field(..., max_length=11, min_length=11, description="联系电话")


class MessageSchema(ModelSchema):
    class Meta:
        model = Message
        fields = "__all__"


class ProgressSchema(ModelSchema):
    class Meta:
        model = Progress
        fields = "__all__"


class CertificateSchema(ModelSchema):
    class Meta:
        model = Certificate
        fields = "__all__"


class EvaluationSchema(ModelSchema):
    class Meta:
        model = Evaluation
        fields = "__all__"


class OrderSchema(ModelSchema):
    class Meta:
        model = Order
        fields = "__all__"


class InvoiceSchema(ModelSchema):
    class Meta:
        model = Invoice
        fields = "__all__"


class ActTypeEnum(Enum):
    TYPE_1 = 1
    TYPE_2 = 2


class UserHubSchema(Schema):
    course_id: int = Field(..., description="课程ID")
    act_type: ActTypeEnum = Field(ActTypeEnum.TYPE_1, description="操作类型")
    is_add: bool = Field(True, description="是否新增")


class CourseOrderSubmitSchema(Schema):
    course_id: int = Field(..., description="课程ID")
    pay_type: str = Field(..., description="支付方式（wechat/alipay）")
    pay_serial_no: str = Field(..., description="支付流水号")


class VipOrderSubmitSchema(Schema):
    vip_product_id: int = Field(..., description="VIP产品ID")
    pay_type: str = Field(..., description="支付方式")
    pay_serial_no: str = Field(..., description="支付流水号")
