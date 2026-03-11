"""
发送邮件的智能体
"""
import os
from dotenv import load_dotenv
from tool.send_email_tool import send_email
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent  # 1.0+ 统一接口

# 加载环境变量
load_dotenv("stu_agent.env")
openai_api_key = os.getenv("OPENAI_API_KEY")

# ---------- 创建智能体流程 ----------

# 1. 定义工具
tools = [send_email]

# 2. 初始化LLM
llm = ChatOpenAI(
    model="qwen3.5-flash",
    api_key=openai_api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)

# 3. 定义提示词
prompt = """
你是一个邮件发送助手，你有一个工具send_email，你可以使用它来发送邮件。
你需要根据用户的指令，调用send_email工具来发送邮件。
用户指令：{instruction}
"""

# 4. 创建智能体
agent = create_agent(model=llm,tools=tools,system_prompt=prompt)

# 5. 运行智能体：invoke 非流式
info = """
请给邮箱：xx@qq.com，发送一封邮件，主题是：Agent向你问好，内容是：新年好！"""
result = agent.invoke({"messages": {"role": "user","content": info,}})
print("AI回复：", result["messages"][-1].content)
