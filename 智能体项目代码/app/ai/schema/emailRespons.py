from pydantic import BaseModel,Field


class EmailRespoanse(BaseModel):
    data:str = Field(...,description="验证码")
    code:str = Field(...,description="状态码")
    msg:str = Field(...,description="提示信息")