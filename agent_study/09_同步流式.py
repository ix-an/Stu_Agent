from tool.mysql_tool import mysql_tool
from utils.model import QwenModel
from langchain.agents import create_agent

def test():
    tools = [mysql_tool]    
    model = QwenModel().model
    prompt = "你是一个数据查询助手，你有一个工具 mysql_tool"
    agent = create_agent(
        model = model,
        tools = tools,
        system_prompt = prompt,
    )
    question = "帮我查询2024年7月份的销售数据"

    # 执行智能体：采用同步流式输出
    data_list = agent.stream(
        {"messages": {"role": "user","content": question,}},
        stream_mode="messages",  # 按消息块返回模型输出
    )
    for chunk, metadata in data_list:
        # chunk:消息块
        # metadata:元数据
        print(chunk.content, end="")

if __name__ == "__main__":
    test()
