from fastapi import FastAPI
from app.utils.logger import Logger
import uvicorn
import sys
from app.ai.agent.system_agent import SystemAgent
from app.ai.agent.signup_agent import SignupAgent
from app.ai.agent.insert_agent import InsertAgent
from app.ai.agent.sql_question_agent import SqlQuestionAgent
from app.ai.agent.sql_question_agent_pg import SqlQuestionAgentPg
from app.ai.agent.echarts_agent import EchartsAgent
from app.ai.agent.anlyze_agent import AnlyzeAgent
from app.ai.agent.file_anlyze_agent import FileAnalyzeAgent
from contextlib import asynccontextmanager 
from fastapi.middleware.cors import CORSMiddleware
from app.api.system.system_router import system_router
from app.api.chat.chat_router import chat_router
from fastapi.staticfiles import StaticFiles
import os

logger = Logger.get_logger(__name__)


@asynccontextmanager
async def create_agent_instance(app:FastAPI):
    app.state.system_agent = SystemAgent()
    app.state.signup_agent = SignupAgent()
    app.state.insert_agent = InsertAgent()
    app.state.sql_question_agent = SqlQuestionAgent()
    app.state.sql_question_agent_pg = SqlQuestionAgentPg()
    app.state.echarts_agent = EchartsAgent()
    app.state.anlyze_agent = AnlyzeAgent()
    app.state.file_analyze_agent = FileAnalyzeAgent()
    logger.info("创建智能体实例成功")
    logger.info("sql智能体实例成功")
    yield
    logger.info("创建智能体实例失败")
    logger.info("sql智能体实例失败")



app = FastAPI(lifespan=create_agent_instance)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 拼接出 static 目录的绝对路径
STATIC_DIR = os.path.join(BASE_DIR, "static")
DOWNLOAD_DIR = os.path.join(STATIC_DIR, "download")

# 确保目录存在（如果不存在会自动创建）
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# --------------------------
# 2. 挂载静态文件服务
# --------------------------
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/favicon.ico")
async def favicon():
    return None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # 前端应用地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system_router)
app.include_router(chat_router)


if __name__ == "__main__":
    # uvicorn.run(app,host="localhost",port=8000)
    cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--loop", "asyncio"]
    import subprocess
    subprocess.run(cmd)