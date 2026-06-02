from app.utils.logger import Logger
from app.ai.model.model import MyModel
from app.ai.tool.mysql_tool import mysql_tool
from app.ai.tool.email_tool import send_email
from langchain.agents import create_agent
from app.ai.schema.emailRespons import EmailRespoanse


logger = Logger.get_logger(__name__)

"""
登录验证码智能体
"""

class SystemAgent:
    #初始化
    def __init__(self):
        logger.info("初始化登录验证码智能体")
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
            一:你是一个登录验证助手,你有两个工具
                1.mysql_tool 执行sql查询
                2.send_email 邮件发送
            二:工作流程:你必须严格按照以下步骤执行
                1.根据用户问题,调用 mysql_tool 工具查询 user_info 表确认邮箱是否存在
                2.调用 send_email 工具发送邮件,邮件内容必须是一个随机不规则的4位数组成的验证码
            三:反馈信息
                1.如果mysql_tool 工具验证邮箱失败,请返回状态码500,验证码位0,提示信息是;邮箱未注册
                2.如果 send_email 工具 发送邮件成功, 请返回状态码200,提示信息是:发送成功
                3.如果 send_email 工具 发送邮件失败, 请返回状态码500,提示信息是:失败原因说明
            【最重要的规则】
                1. 邮件只允许发送 1 次，绝对不能重复发送！
                3. 绝对不能循环执行！
        """
        self.agent = create_agent(model=self.model,system_prompt=prompt,tools=self.tools,response_format=EmailRespoanse)
        return self.agent

    #运行智能体
    def answer(self,question):
        rs = self.agent.invoke({"messages":[{"role":"user","content":question}]})
        # print(",,,,,,,,,",rs)
        answer = rs["structured_response"].model_dump()
        logger.info(f"智能体返回结果：{answer}")
        return answer


if __name__ == "__main__":
    agnet = SystemAgent()
    agnet.answer("用户邮箱是：3327354636@qq.com")