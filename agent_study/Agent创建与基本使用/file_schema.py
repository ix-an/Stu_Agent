from pydantic import BaseModel, Field

# 文件操作工具的模型参数
class FileSchema(BaseModel):
    path: str = Field(..., description="文件路径")