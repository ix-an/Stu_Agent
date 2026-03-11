import os
from dotenv import load_dotenv
from tool.file_tool import open_dir, open_video
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent 

# 加载环境变量
load_dotenv("stu_agent.env")
openai_api_key = os.getenv("OPENAI_API_KEY")

# 定义工具
tools = [open_dir, open_video]

# 实例化大模型
llm = ChatOpenAI(
    model="qwen3.5-flash",
    api_key=openai_api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0,
)

# 定义提示词
prompt = """
一：你是一个可以控制电脑文件的智能体。
二：你可以使用以下工具：
1. open_dir：打开文件夹，文件夹不存在则自动创建
2. open_video：打开视频文件
"""

# 创建智能体
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=prompt,
    debug=True,
)

if __name__ == "__main__":
    # 测试智能体
    q1 = "打开D盘下的 test_agent 文件夹"
    result = agent.invoke({"messages": {"role": "user","content": q1,}})
    print(result)    
    q2 = "打开 'D:\素材\视频\Tokyo.mp4' 视频文件"
    result = agent.invoke({"messages": {"role": "user","content": q2,}})
    print(result)