"""
LangChain 1.0 Agent + PostgreSQL Memory 示例

目标：
理解如何使用 PostgreSQL 持久化存储 Agent 的对话记忆

核心知识：
1. Checkpointer：负责保存 Agent 状态
2. thread_id：区分不同对话线程
3. PostgresSaver：将 Agent 状态保存到 PostgreSQL
"""

from dotenv import load_dotenv
import os

from utils.model import QwenModel
from tool.mysql_tool import mysql_tool
from langchain.agents import create_agent

# PostgreSQL Checkpointer
from langgraph.checkpoint.postgres import PostgresSaver


# =========================
# 1 加载环境变量
# =========================
load_dotenv("stu_agent.env")

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
DB = os.getenv("POSTGRES_DB")

POSTGRES_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}?sslmode=disable"


# =========================
# 2 初始化模型
# =========================
model = QwenModel().model
system_prompt = "你是一个数据库查询助手"

# =========================
# 3 创建 Postgres Checkpointer
# =========================

"""
PostgresSaver

作用：
将 Agent 的运行状态保存到 PostgreSQL

保存内容：
- messages（对话历史）
- state（Agent状态）
- thread_id（会话ID）

优点：
✔ 数据持久化
✔ 支持多实例
✔ 可用于生产环境
"""

with PostgresSaver.from_conn_string(POSTGRES_URL) as checkpointer:

    # 初始化数据库表
    checkpointer.setup()

    # =========================
    # 4 创建 Agent
    # =========================
    agent = create_agent(
        model=model,
        tools=[mysql_tool],
        system_prompt=system_prompt,
        debug=False,
        checkpointer=checkpointer,  # 关键：启用持久化记忆
    )

    # =========================
    # 5 封装对话函数
    # =========================
    def chat(question: str):

        """
        invoke 时必须指定 thread_id
        thread_id 相同 → 共享记忆
        """
        result = agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
            {
                "configurable": {
                    "thread_id": "user_1"
                }
            }
        )

        print(result["messages"][-1].content)

    # =========================
    # 6 测试多轮对话
    # =========================
    # questions = ["我叫张三","请问我叫什么名字？"] 
    questions = ["请问我叫什么名字？"]  # 本地存储记忆测试
    for q in questions:
        chat(q)
        print("=" * 40)