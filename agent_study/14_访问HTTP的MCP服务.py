from fastmcp import Client
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from utils.model import QwenModel
import asyncio


# 老版调用：定义异步函数
async def test():
    # 创建一个客户端
    async with Client("http://localhost:9000/mcp") as client:
        # 获取工具列表
        tools = await client.list_tools()
        print(tools)
        # 调用工具
        result = await client.call_tool("add_number", {"a": 1, "b": 2})
        print(result)
        print(result.data)

# langchain 1.0 调用
async def test_langchain():
    model = QwenModel().model
    prompt = "你是一个智能助手"

    # 定义连接MCP服务的配置
    client = MultiServerMCPClient(
        {
            "test": {
                "transport": "http",
                "url": "http://localhost:9000/mcp"
            }
        }
    )

    # 获取工具列表
    tools = await client.get_tools()
    print(tools)

    # 创建智能体
    agent = create_agent(model=model, system_prompt=prompt, tools=tools)
    question = "2+3=?"
    # MCP是异步的，使用 ainvoke 方法调用
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)

if __name__ == '__main__':
    asyncio.run(test_langchain())
