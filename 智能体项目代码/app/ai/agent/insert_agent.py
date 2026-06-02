from app.utils.logger import Logger
from app.ai.model.model import MyModel
from app.ai.tool.mysql_tool import mysql_tool
from app.ai.tool.email_tool import send_email
from langchain.agents import create_agent
from app.ai.schema.emailRespons import EmailRespoanse


logger = Logger.get_logger(__name__)

"""
数据库写入智能体
"""

class InsertAgent:
    #初始化
    def __init__(self):
        logger.info("数据库写入智能体")
        self.model = MyModel.get_model()
        self.tools = self.init_tool()
        self.agent = self.init_agent()
    
    #初始化工具
    def init_tool(self):
        self.tools = [mysql_tool,send_email]
        return self.tools
    #创建智能体
    def init_agent(self):
        prompt = """
            一:你是一个数据库写入助手,你有一个工具
                1.mysql_tool 执行sql查询
            二:工作流程:你必须严格按照以下步骤执行
                1.根据用户提供的信息,调用 mysql_tool 工具,将用户信息写入user_info表中
            三:反馈信息
                1.如果mysql_tool 工具写入成功,请返回状态码200,提示信息是:写入成功
                2.如果 mysql_tool 工具 写入失败, 请返回状态码500,提示信息是:失败原因说明
            【最重要的规则】
                1. 写入只允许进行 1 次，绝对不能重复写入！
                3. 绝对不能循环执行！
        """
        self.agent = create_agent(model=self.model,system_prompt=prompt,tools=self.tools,response_format=EmailRespoanse)
        return self.agent

    #运行智能体
    def answer(self,question):
        rs = self.agent.invoke({"messages":[{"role":"user","content":question}]})
        # print(",,,,,,,,,",rs)
        answer = rs["messages"][-1].content
        logger.info(f"智能体返回结果：{answer}")
        return answer


if __name__ == "__main__":
    agnet = InsertAgent()
    agnet.answer("姓名是李四，邮箱是3327354636@qq.com")