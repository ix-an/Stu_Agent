from pydantic import BaseModel, Field

# mysql工具的模型参数
class MySqlSchema(BaseModel):
    sql:str = Field(..., description="mysql语句")
    