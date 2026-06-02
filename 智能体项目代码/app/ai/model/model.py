from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class MyModel:
    _model = None

    @staticmethod
    def get_model():
        if MyModel._model is None:
            MyModel._model = ChatOpenAI(
                model=os.getenv("MODEL_NAME"),
                api_key=os.getenv("MODEL_KEY"),
                base_url=os.getenv("MODEL_URL"),
                #streaming=True,
    # model_kwargs={
    #     "extra_body": {
    #         "thinking": {"type": "disabled"},  # 开启思考模式
    #         "reasoning_effort": "high"       # 可选：设置思考强度（high/max）
    #     }
    # }
            )
        return MyModel._model