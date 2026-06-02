from app.utils.logger import Logger
from app.ai.model.model import MyModel
from app.ai.tool.mysql_tool import mysql_tool
from langchain.agents import create_agent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from app.utils.permision_middle import before_agent_middleware
import asyncio
from dotenv import load_dotenv
import os
from langchain.messages import HumanMessage

load_dotenv()

logger = Logger.get_logger(__name__)

"""
aql(生产级) 问答智能体
"""
class SqlQuestionAgentPg:

    def __init__(self):
        logger.info("初始化 SQL 问答智能体")
        self.model = MyModel.get_model()
        self.tools = self.init_tool()
        

    def init_tool(self):
        self.tools = [mysql_tool]
        return self.tools
    

    async def answer(self,question:str,user_id:str):
        prompt = """
                一：你是一个 SQL 问答助手，你有一个工具 mysql_tool
                二：重要规则：
                    -只能使用select语句查询数据，绝对不能执行任何修改数据的语句（如insert、update、delete等）
                三：使用规则
                    -如果查询销售数据，请查询 sales 表
                    - 多表查询时使用正确的JOIN关系
                """
        user = os.getenv("POSTGRSSQL_USER")
        password = os.getenv("POSTGRSSQL_paw")
        host = os.getenv("POSTGRSSQL_HOST")
        db = os.getenv("POSTGRSSQL_DATABASE")
        url = f"postgresql://{user}:{password}@{host}:5432/{db}?sslmode=disable"
        async with AsyncPostgresSaver.from_conn_string(url) as pg:
            await pg.setup()
            agent = create_agent(model=self.model,system_prompt=prompt,tools=self.tools,checkpointer=pg,middleware=[before_agent_middleware])
            msg = HumanMessage(content=question,user_id=user_id)
            try:
                rs = agent.astream({"messages":[msg]},
                                    {"configurable":{"thread_id":user_id}},
                                    stream_mode="messages")
                async for c,m in rs:
                        if not hasattr(c,"tool_call_id"):
                            yield c.content
            except Exception as e:
                logger.error(e)
                yield str(e)
                

if __name__ == "__main__":
    import asyncio
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    agnet = SqlQuestionAgentPg()


    async def test():
        text = "请向用户表插入一条数据：用户名：威威，邮箱是132154@qq.com"
        text2 = "查询2023年1月销售前5的商品类型"
        async for c in agnet.answer(text2,"3327354636@qq.com"):
            print(c,end="")
    asyncio.run(test())
