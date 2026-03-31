from langchain.agents.middleware import (
    before_model,
    after_model,
    before_agent,
    after_agent,
    AgentState,
)
from langgraph.runtime import Runtime
from utils.model import QwenModel
from tool.send_email_tool import send_email
from langchain.agents import create_agent

# 调用计数器（生产环境应使用数据库缓存）
i = 0
max_calls = 3

@before_agent
def before_agent(state: AgentState, runtime: Runtime) -> dict | None:
    print("agent调用前中间件")
    if i >= max_calls:
        raise Exception("agent调用次数超过限制")
    return None

@after_agent
def after_agent(state: AgentState, runtime: Runtime) -> dict | None:
    print("agent调用后中间件")
    global i
    i += 1
    print(f"当前调用次数: {i}")
    return None

@before_model
def before_model(state: AgentState, runtime: Runtime) -> dict | None:
    print("模型调用前中间件")
    return None

@after_model
def after_model(state: AgentState, runtime: Runtime) -> dict | None:
    print("模型调用后中间件")
    return None

def test():
    try:
        model = QwenModel().model
        tools = [send_email]
        prompt = "你是一个智能助手"
        middleware = [before_agent, after_agent, before_model, after_model]
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=prompt,
            middleware=middleware,
        )
        # 执行agent
        q = "你好。"
        r = agent.invoke({"messages": [{"role": "user", "content": q}]})
        print(r["messages"][-1].content)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    for i in range(5):
        test()
        print("-" * 20)


