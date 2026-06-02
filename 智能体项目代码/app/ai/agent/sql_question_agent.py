from app.utils.logger import Logger
from app.ai.model.model import MyModel
from app.ai.tool.mysql_tool import mysql_tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import asyncio

logger = Logger.get_logger(__name__)

"""
aql 问答智能体
"""
class SqlQuestionAgent:

    def __init__(self):
        logger.info("初始化 SQL 问答智能体")
        self.model = MyModel.get_model()
        self.tools = self.init_tool()
        self.agent = self.init_agent()

    def init_tool(self):
        self.tools = [mysql_tool]
        return self.tools
    
    def init_agent(self):
        prompt = """
                一：你是一个 SQL 问答助手，你有一个工具 mysql_tool
                """
        agent = create_agent(model=self.model,system_prompt=prompt,tools=self.tools,checkpointer=InMemorySaver())
        return agent


    async def answer(self,question:str,user_id:int):
        rs = self.agent.astream({"messages":[{"role":"user","content":question}]},
                                {"configurable":{"thread_id":user_id}},
                                stream_mode="messages")
        async for c,m in rs:
            if not hasattr(c,"tool_call_id"):
                yield c.content
            

if __name__ == "__main__":
    agnet = SqlQuestionAgent()
    import asyncio
    async def test():
        async for c in agnet.answer("李四年龄是多少",1):
            print(c,end="")
    asyncio.run(test())
