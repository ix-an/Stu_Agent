from langchain.agents.middleware import after_model, AgentState
from langgraph.runtime import Runtime
from langchain.messages import AIMessage
from typing import Any
from utils.model import QwenModel
from tool.send_email_tool import send_email
from langchain.agents import create_agent
import re

@after_model
def filter_sensitive_words(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    # after_model的 state包含模型输出 AIMessage
    print(f"state:\n {state}")
    print(f"runtime:\n {runtime}")
    ai_message = state["messages"][-1].content
    # 过滤敏感词
    sensitive_words = ["a", "b", "c"]
    for word in sensitive_words:
        # 如果AI回复中有敏感词
        if word in ai_message:
            print(f"模型输出中包含敏感词：{word}")
            # 过滤掉敏感词
            res = re.sub(word, "*" * len(word), ai_message)
            return {"messages": [AIMessage(content=res)]}
    return None

def test():
    model = QwenModel().model
    tools = [send_email]
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="你是一个智能助手，你有一个工具send_email用于发送邮件，其他问题请直接回答",
        middleware=[filter_sensitive_words],
    )
    q = "我叫bb，请向我问好。"
    result = agent.invoke({"messages": {"role": "user", "content": q}})
    print("\n模型输出:\n", result["messages"][-1].content)

if __name__ == "__main__":
    test()
