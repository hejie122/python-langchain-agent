from fastapi import APIRouter
from app.utils.logger import Logger
from fastapi import Request
from fastapi.responses import StreamingResponse
import json

logger = Logger.get_logger(__name__)

chat_router = APIRouter()

@chat_router.get("/chat")
async def chat(request:Request, question:str,user_id:str):
    #根据用户问题判断使用哪个智能体
    if "图表" in question:
        echarts_agent = request.app.state.echarts_agent
        return echarts_agent.answer(question,user_id)
    elif "数据分析" in question:
        anlyze_agent = request.app.state.anlyze_agent
        data = anlyze_agent.answer(question,user_id)
        return {"code":200,"data":data}
    else:
        if "上传文件成功" in question:
            agent = request.app.state.file_analyze_agent
        else:
            # sql_question_agent = request.app.state.sql_question_agent
            agent = request.app.state.sql_question_agent_pg
        async def gennerate():
            try:
                async for chunk in agent.answer(question,user_id):
                    msg = {"content":chunk,"done":False}
                    yield f"data:{json.dumps(msg)}\n\n"

                msg = {"content":"","done":True}
                yield f"data:{json.dumps(msg)}\n\n"
            except Exception as e:
                logger.error(f"智能体处理请求时发生错误：{e}")
                msg = {"content":"智能体处理请求时发生错误，请稍后再试。","done":True,"error":True}
                yield f"data:{json.dumps(msg)}\n\n"
        return StreamingResponse(gennerate(), media_type="text/event-stream")


from fastapi import  UploadFile, File
import os
@chat_router.post("/upload")
async def upload(file: UploadFile = File(...)):
    # 上传目录
    UPLOAD_DIR = "app/static/upload"
    # 创建上传目录
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    # 创建文件全路径
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    logger.info(f"上传文件：{file_path}")
    # 保存文件
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "code": 200,
        "filename": file.filename
    }