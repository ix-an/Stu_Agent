from fastmcp import FastMCP

# 创建一个 FastMCP 实例
mcp = FastMCP("服务器_测试")

# 定义工具
@mcp.tool(name="add_number",description="两个数字相加")
# name 默认为函数名，description 默认为函数的docstring
def add_number(a:float,b:float)->float:
    """
    加法计算器，两个数相加
    """
    return a + b

# 启动 http 服务器
mcp.run(
    host="localhost",
    transport="http",
    port=9000,
)
