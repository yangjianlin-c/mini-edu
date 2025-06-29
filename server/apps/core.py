from ninja.errors import AuthenticationError
from datetime import datetime, timezone, timedelta
from typing import Any, Generic, TypeVar, Optional
import jwt
from ninja.security import HttpBearer
from apps.user.models import User
from pydantic import BaseModel
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.conf import settings

T = TypeVar("T")


class R(BaseModel, Generic[T]):
    code: int = 1
    data: Optional[T] = None
    msg: str = "ok"

    @classmethod
    def ok(cls, data: T = None, msg="ok") -> "R":
        return cls(code=1, data=data, msg=msg)

    @classmethod
    def fail(cls, msg: str = "fail") -> "R":
        return cls(code=0, msg=msg)


class TokenUtil:
    def __init__(
        self,
    ):
        self.secret_key = settings.JWT_SECRET_KEY
        self.effective_time = settings.JWT_EXPIRATION_TIME
        self.algorithms = settings.JWT_ALGORITHM

    def build(self, payload: Any) -> str:
        """
        生成token
        :param payload: 加密数据
        :return: token
        """
        data = {
            "exp": datetime.now(tz=timezone.utc)
            + timedelta(seconds=self.effective_time),
            "payload": payload,
        }
        return jwt.encode(data, self.secret_key, self.algorithms)

    def parse(self, token: str) -> Any:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.algorithms)
            return payload.get("payload")
        except ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except InvalidTokenError:
            raise AuthenticationError("Invalid token")
        except Exception as e:
            raise AuthenticationError(f"Token parsing error: {str(e)}")


token_util = TokenUtil()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_id = token_util.parse(token)
            request.user = User.objects.get(id=user_id)
            return user_id
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise AuthenticationError(f"Token error: {str(e)}")
        except User.DoesNotExist:
            raise AuthenticationError("User not found for this token")
        except Exception as e:
            raise AuthenticationError(f"Unexpected error: {str(e)}")


auth = dict(auth=AuthBearer())
