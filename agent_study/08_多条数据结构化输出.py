from pydantic import BaseModel,Field
from tool.mysql_tool import mysql_tool
from utils.model import QwenModel
from langchain.agents import create_agent

# 产品类
class ProductResponse(BaseModel):
    product_name:str = Field(...,description="产品名称")
    category:str = Field(...,description="产品类别")
    quantity:int = Field(...,description="产品数量")
# 订单类（列表）
class ProductList(BaseModel):
    product_list : list[ProductResponse] = Field(...,description="产品列表")


def test():
    tools = [mysql_tool]
    model = QwenModel().model
    prompt =  "你是一个数据查询助手，你有一个工具 mysql_tool"
    agent = create_agent(
        model = model,
        tools = tools,
        system_prompt = prompt,
        response_format=ProductList
    )
    question = "帮我查询2024年7月份的销售数据"
    result = agent.invoke({"messages": {"role": "user","content": question,}})
    answer = result["structured_response"].model_dump()
    print("结构化输出：", answer)
    for product in answer["product_list"]:
        print(product)

if __name__ == "__main__":
    test()
    
