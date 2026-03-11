import os
from dotenv import load_dotenv
from tool.send_email_tool import send_email
from tool.mysql_tool import mysql_tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent 

# 加载环境变量
load_dotenv("stu_agent.env")
openai_api_key = os.getenv("OPENAI_API_KEY")

# 定义工具
tools = [mysql_tool, send_email]
# 实例化大模型
llm = ChatOpenAI(
    model="qwen3.5-flash",
    api_key=openai_api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)

# ----- 以上步骤完全一致 -----
# ----- 加载环境变量，导入工具，定义工具，实例化大模型 -----

# ReAct模式关键在于定义提示词，告诉LLM如何利用工具完成任务
# 目标：查询销售额，发到 “我的” 邮箱

# 定义提示词
prompt = """
一、角色定位：你是一个邮件发送助手，专门负责发送邮件。
二、可使用的工具：
    1. mysql_tool(sql: str) -> str: 执行mysql语句，返回执行结果
    2. send_email(to: str, subject: str, content: str) -> str: 发送邮件，返回发送结果
三、工作流程：
    1. 分析用户请求，提取用户名
    2. 使用mysql_tool执行SQL查询：SELECT email FROM user_info WHERE user_name = '用户名'
    3. 解析查询结果，提取邮箱地址
    - 查询结果格式可能是：((email,),) 或类似格式
    - 请从结果中提取出纯邮箱地址
    4. 验证邮箱地址是否包含@符号
    5. 构建邮件内容
    6. 使用send_email发送邮件
四、邮件发送规则：
    1. 收件人邮箱必须验证是否包含@符号。
    2. 邮件主题为：{user_name} 的销售数据
    3. 邮件内容包含：
        - 销售详细数据
        - 销售计划
        - 销售数据分析
    4. 邮件发送成功，返回成功信息。
    5. 邮件发送失败，返回失败信息。
    6. 如果用户提到“我的”，对象指数据库里的 xx
"""

# 定义智能体
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=prompt,
    debug=True,  # 显示大模型思考过程
)

# 执行智能体
question = "帮我查询 2024 年 7 月的销售额，然后发到我的邮箱"
result = agent.invoke({"messages": {"role": "user","content": question,}})
print("输出结果：", result["messages"][-1].content)