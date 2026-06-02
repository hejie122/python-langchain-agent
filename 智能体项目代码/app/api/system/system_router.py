from fastapi import APIRouter
from app.api.schema.Login_schema import *
from app.utils.logger import Logger
from fastapi import Request
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

system_router = APIRouter()

logger = Logger.get_logger(__name__)

#定义一个登录接口
@system_router.post("/send_code")
def send_code(request:Request, args:SendCodeSchema):
    agent = request.app.state.system_agent
    rs = agent.answer(args.email)
    # print(",,,,,,,,,",rs)
    redis_client.set(f"{args.email}:code",rs['data'],60)
    logger.info(f"验证码发送成功，存储成功")
    return {"code":rs["code"],"msg":rs["msg"]}

@system_router.post("/login")
def login(request:Request, args:LoginSchema):
    logger.info(f"字节码:{redis_client.get(f"{args.email}:code")}")
    try:
        code = redis_client.get(f"{args.email}:code").decode()
        if code == args.code:
            return {"code":200,"msg":"登录成功"}
        return {"code":500,"msg":"登录失败，验证码错误"}
    except Exception as e:
        logger.warning(f"验证码超过1分钟，请重新获取：{e}")
        return {"code":500,"msg":"验证码不存在或已过期"}


@system_router.post("/signup_sendemail")
def signup_sendemail(request:Request, args:signup_SendCodeSchema):
    agent = request.app.state.signup_agent
    rs = agent.answer(args.email)
    # print(",,,,,,,,,",rs)
    redis_client.set(f"{args.email}:code",rs['data'],60)
    logger.info(f"验证码发送成功，存储成功")
    return {"code":rs["code"],"msg":rs["msg"]}


@system_router.post("/signup")
def signup(request:Request, args:SignupSchema):
    logger.info(f"字节码:{redis_client.get(f"{args.email}:code")}")
    try:
        code = redis_client.get(f"{args.email}:code").decode()
        if code == args.code:
            agent = request.app.state.insert_agent
            rs = agent.answer(f"姓名是{args.name}，邮箱是{args.email}")
            logger.info(f"用户信息写入结果：{rs}")
            return {"code":200,"msg":"注册成功"}
        return {"code":500,"msg":"注册失败，验证码错误"}
    except Exception as e:
        logger.warning(f"验证码超过1分钟，请重新获取：{e}")
        return {"code":500,"msg":"验证码不存在或已过期"}
    