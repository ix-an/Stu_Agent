from pydantic import BaseModel,Field
from tool.send_email_tool import send_email
from utils.model import QwenModel
from langchain.agents import create_agent

# 定义格式邮件发送智能体的格式输出 BaseModel
class EmailResponse(BaseModel):
    data:str = Field(...,description="验证码")
    code:str = Field(...,description="状态码")
    msg:str = Field(...,description="提示信息")

# 定义邮件发送智能体
tools = [send_email]
model = QwenModel().model
prompt = """
一 ： 你是一个通过邮箱发送验证码的助手
二 ： 你有一个工具： send_email 发送邮件
三 : 工作流程：
    用户接收到邮箱后，请按照下面步骤执行
    1、构建邮件内容：随机生成4位数字的不规则验证码，邮件内容示例：你的验证码是 xxxx
    2、如果邮件发送成功，请提示用户：邮件发送成功，状态码是200
    3、如果邮件发送失败，请提示用户：失败原因，状态是500
"""
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=prompt,
    response_format=EmailResponse,  # 结构化输出
)

# 执行智能体
question = "邮箱：536001397@qq.com"
result = agent.invoke({"messages": {"role": "user","content": question,}})
# model_dump() 方法将 Pydantic 模型转换为字典
answer = result["structured_response"].model_dump()  
print("结构化输出：", answer)
print("输出类型：", type(answer))
print("内容：", answer["data"])
