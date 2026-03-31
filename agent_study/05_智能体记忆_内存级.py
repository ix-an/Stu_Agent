"""
LangChain 1.0 Agent Memory 示例

核心目标：
理解 LangChain 1.0 如何通过 Checkpointer 实现对话记忆

关键概念：
1. Checkpointer：负责保存 Agent 的状态
2. thread_id：用于区分不同对话线程
3. InMemorySaver：内存级存储（仅测试用）
"""

from utils.model import QwenModel
from tool.mysql_tool import mysql_tool
from langchain.agents import create_agent
# LangGraph 提供的记忆存储组件
from langgraph.checkpoint.memory import InMemorySaver


model = QwenModel().model
prompt = "你是一个数据库查询助手"
memory_saver = InMemorySaver()  # 创建记忆存储器

# 创建智能体
agent = create_agent(
    model=model,
    system_prompt=prompt,
    tools=[mysql_tool],
    debug=False,
    checkpointer=memory_saver,  # 启用记忆
)

def test(qs):
    result = agent.invoke(
        input={"messages": [{"role": "user", "content": qs}]},
        config={
            "configurable": {
                "thread_id": "10"  # 核心：指定记忆的线程ID，同一ID复用记忆
                # 可选：添加 session_id 等扩展字段，增强记忆隔离性
            }
        },  

    )
    print(result["messages"][-1].content)

if __name__ == "__main__":
    question =[
        "我叫张三，你是谁",
        "请问，我叫什么名字"
    ]
    for q in question:
        test(q)
        print("=="*20)
