from app.utils.logger import Logger
from app.ai.model.model import MyModel
from app.ai.tool.docx_read_tool import docx_read_tool
from app.ai.tool.docx_write_tool import docx_write_tool
from langchain.agents import create_agent
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate

load_dotenv()

logger = Logger.get_logger(__name__)

"""
文件数据分析智能体
"""
class FileAnalyzeAgent:

    def __init__(self):
        logger.info("初始化文件数据分析智能体")
        self.model = MyModel.get_model()
        self.tools = self.init_tool()

    def init_tool(self):
        self.tools = [docx_read_tool,docx_write_tool]
        return self.tools



    async def answer(self,question:str,user_id:str):
        prompt="""
            一 你是一个AI数据分析助手，你有两个工具：
              1 docx_read_tool 
              2 docx_write_tool
           二 工作流程
              1 请用 docx_read_tool 工具读取 docx 文件，文件路径是：{path}
              2 请分析一下文件内容，查看是否有数据缺失和数据重复，如果有，填充缺失值，缺失值填充：None，删除数据重复
              3 调用 docx_write_tool 工具 将 分析后的数据写入到文档中
           三：反馈信息
               请返回分析文件内容
        """
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        # 上传目录的路径
        upload_dir = BASE_DIR / "static/upload"
        #获取文件名的全路径
        path = os.path.join(upload_dir, question.split(":")[1])
        logger.info(f"上传文件路径：{path}")
        # 创建提示词
        prompt_temple = PromptTemplate.from_template(prompt)
        # 传入变量
        system_prompt = prompt_temple.format(path=path)
        agent = create_agent(model=self.model,system_prompt=system_prompt,tools=self.tools)
        async for c,m in agent.astream({"messages":[{"role":"user","content":question}]},
                                       stream_mode="messages"):
            if not hasattr(c,"tool_call_id"):
                yield c.content

if __name__ == "__main__":
    agnet = FileAnalyzeAgent()
    import asyncio
    async def test():
        async for c in agnet.answer("上传文件成功:word.docx"):
            print(c,end="")
    asyncio.run(test())
