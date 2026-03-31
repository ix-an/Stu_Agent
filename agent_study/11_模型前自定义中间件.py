from langchain.agents.middleware import before_model, AgentState
from langgraph.runtime import Runtime
from typing import Any
from utils.model import QwenModel
from tool.send_email_tool import send_email
from langchain.agents import create_agent


@before_model
def check_sensitive_words(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    # 查看参数信息
    print(f"state:\n {state}")
    print(f"runtime:\n {runtime}")

    # 从“数据库”提取敏感词
    sensitive_words = ["a", "b", "c"]
    # 获取用户问题
    question = state["messages"][-1].content
    for word in sensitive_words:
        if word in question:
            print(f"用户问题中包含敏感词：{word}")
            # before_model 只能抛出异常，无法返回 AIMessages
            raise ValueError("用户问题中包含敏感词，请换个问题")
    return None

def test():
    try:
        model = QwenModel().model
        tools = [send_email]
        agent = create_agent(
            model = model,
            tools = tools,
            system_prompt = "你是一个邮件发送助手，你有一个工具send_email",
            middleware = [check_sensitive_words],
        )
        q = "你好，a"
        result = agent.invoke({"messages": {"role": "user","content": q}})
        print(result["messages"][-1].content)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    test()
