from pydantic import BaseModel,Field


"""
发送验证码接口的参数模型类
"""
class SendCodeSchema(BaseModel):
    email: str = Field(...,description="邮箱")

""""
登录验证码接口的参数模型类
"""
class LoginSchema(BaseModel):
    email: str = Field(...,description="邮箱")
    code: str = Field(...,description="验证码")

"""
注册发送验证码接口的参数模型类
"""
class signup_SendCodeSchema(BaseModel):
    email: str = Field(...,description="邮箱")


"""
注册接口的参数模型类
"""
class SignupSchema(BaseModel):
    name: str = Field(...,description="姓名")
    email: str = Field(...,description="邮箱")
    code: str = Field(...,description="验证码")
