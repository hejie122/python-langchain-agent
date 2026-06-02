from langchain.agents.middleware import before_agent
from langchain.agents import AgentState
from langgraph.runtime import Runtime
from app.utils.logger import Logger
from app.utils.permmision_role import permission_role

logger = Logger.get_logger(__name__)

@before_agent
def before_agent_middleware(state:AgentState, runtime:Runtime):
    print(state)
    user_id = state["messages"][0].user_id
    logger.info(f"用户 {user_id}")
    role = permission_role(user_id)
    if role == None:
        raise Exception("用户不存在，请重新登录")
    if role != "总经理":
        raise Exception("用户没有权限执行该操作")
    return None