from pydantic import BaseModel, Field

# 邮件工具的模型参数
class EmailSchema(BaseModel):
    # ... 代表必须输入
    to: str = Field(..., description="收件人邮箱地址")
    subject: str = Field(..., description="邮件主题")
    content: str = Field(..., description="邮件正文内容")