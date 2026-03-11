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
# 构建提示词
prompt = """
你是一个邮件发送助手，专门负责发送邮件。

你有两个工具：
1. mysql_tool(sql: str) -> str: 执行mysql语句，返回执行结果
   数据库模式：stu_agent.user_info 表：id,user_name,email

2. send_email(to: str, subject: str, content: str) -> str: 发送邮件，返回发送结果

工作流程：
1. 分析用户请求，提取用户名
2. 使用mysql_tool执行SQL查询：SELECT email FROM user_info WHERE user_name = '用户名'
3. 解析查询结果，提取邮箱地址
   - 查询结果格式可能是：((email,),) 或类似格式
   - 请从结果中提取出纯邮箱地址
4. 验证邮箱地址是否包含@
5. 构建邮件内容：用户名 你好。
6. 使用send_email发送邮件
7. 返回邮件发送结果

注意：
- 如果查询不到邮箱，请提示：收件人邮箱地址缺失/错误
- 如果邮箱格式不正确，请提示：收件人邮箱地址缺失/错误
"""
# 定义智能体
agent = create_agent(model=llm,tools=tools,system_prompt=prompt)
# 运行智能体
question = """
给 xx 发一封邮件。
"""
result = agent.invoke({"messages": {"role": "user","content": question,}})
# 输出智能体回复
print(result["messages"][-1].content)

