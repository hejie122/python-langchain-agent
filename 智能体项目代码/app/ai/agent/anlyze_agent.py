from app.utils.logger import Logger
from app.ai.model.model import MyModel
from app.ai.tool.mysql_tool import mysql_tool
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from app.utils.permision_middle import before_agent_middleware
import asyncio
from dotenv import load_dotenv
import os
from langchain.messages import HumanMessage
from app.ai.schema.anlyze_respons import AnalyzeResponse
from app.utils.permision_middle import before_agent_middleware

logger = Logger.get_logger(__name__)
load_dotenv()

"""
    智能分析 图标智能体
"""

class AnlyzeAgent:

    def __init__(self):
        logger.info("初始化 智能分析 图标智能体")
        self.model = MyModel.get_model()
        self.tools = self.init_tool()
        

    def init_tool(self):
        self.tools = [mysql_tool]
        return self.tools
    
    def answer(self,question:str,user_id:str):
        prompt = """
                一:你是一个数据分析助手,你有一个工具:mysql_tool
                二:工作流程:你必须严格按照以下步骤来执行，执行完成后必须立即停止，禁止重复调用工具。
                    步骤一:查询数据,把数据以表格形式存入到表格数据
                    步骤二:根据问题做出数据分析,按照以下格式来分析,把分析结果存入到分析结果 
                        一:详细分析
                            1 xxxx:
                                xxxx
                                xxxx
                            2 XXXX:
                                xxxx
                                xxxx
                        二:结论部分:
                                .xxxxx
                                .xxxxx
                                .xxxxx
                    步骤三:生成一个echarts图表,图表数据json格式必须是以下要求,把数据存入到图表数据 
                        1 返回的数据必须是一个可执行的json格式,其它的文本信息不需要
                        2 返国的图表必须有保存功能
                    三：重要规则
                    	1. **SQL生成规范**:
   				            - 只能使用SELECT查询，禁止使用INSERT/UPDATE/DELETE等修改操作
   			            2. **查询原则**:
   				            - 涉及排名或TOP N时，必须使用ORDER BY和LIMIT
   				            - 多表查询时使用正确的JOIN关系
   				            - 只查询前10条记录
        """

        msg = HumanMessage(content=question,user_id=user_id)

        user = os.getenv("POSTGRSSQL_USER")
        password = os.getenv("POSTGRSSQL_paw")
        host = os.getenv("POSTGRSSQL_HOST")
        db = os.getenv("POSTGRSSQL_DATABASE")
        url = f"postgresql://{user}:{password}@{host}:5432/{db}?sslmode=disable"

        with PostgresSaver.from_conn_string(url) as pg:
            pg.setup() 
            agent = create_agent(model=self.model,
                                 system_prompt=prompt,
                                 tools=self.tools,
                                 checkpointer=pg,
                                 response_format=AnalyzeResponse,
                                 middleware=[before_agent_middleware]
                                 )
            
            try:
                config = {
                    "configurable": {"thread_id": user_id},
                    "recursion_limit": 100  # 这里是修复核心！
                }

                rs = agent.invoke({
                    "messages": [msg]
                }, config=config)
                # rs = agent.invoke({"messages":[msg]},
                #                 {"configurable":{"thread_id":user_id}})
                data = rs["structured_response"].model_dump()
                logger.info(data)
                return data
            except Exception as e:
                logger.error(e)
                return e
        

if __name__ == "__main__":
    agnet = AnlyzeAgent()
    text = "2023年3月份销售数据分析"
    print(agnet.answer(text,"3327354636@qq.com"))
    