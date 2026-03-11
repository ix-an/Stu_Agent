# langchain工具封装包
from langchain.tools import tool
# 邮件工具的模型参数
from .schema.email_schema import EmailSchema
# 发送邮件相关包
import smtplib
from email.mime.text import MIMEText
# 环境导入相关包
from dotenv import load_dotenv
from pathlib import Path
import os

# 加载环境变量
env_path = Path(__file__).parent.parent / "stu_agent.env"
load_dotenv(env_path)
qq_email_auth_code = os.getenv("QQ_EMAIL_AUTH_CODE")  # QQ邮箱授权码
email_host = os.getenv("EMAIL_HOST")  # 邮箱SMTP服务器地址
email_from = os.getenv("EMAIL_FROM")  # 发件人邮箱地址
email_to = os.getenv("EMAIL_TO")  # 收件人邮箱地址


# 定义工具
@tool("send_email", args_schema=EmailSchema)
def send_email(to: str, subject: str, content: str) -> str:
    """
    发送邮件的工具函数
    """
    try:
        # 创建邮件对象
        msg = MIMEText(content, "plain", "utf-8")  # 邮件内容、类型和编码
        # 设置邮件头
        msg["Subject"] = subject  # 邮件主题
        msg["From"] = email_from  # 发件人邮箱
        msg["To"] = to  # 收件人邮箱
        # 创建SMTP对象
        smtp = smtplib.SMTP_SSL(email_host, 465)
        # 登录SMTP服务器：qq邮件服务
        smtp.login(email_from, qq_email_auth_code)  # 发件人邮箱和授权码
        # 发送邮件（发件人，收件人，邮件对象_str格式）
        smtp.sendmail(email_from, to, msg.as_string())
        print("邮件发送成功")
        return "邮件发送成功"
    except Exception as e:
        print("邮件发送失败：", e)
        return "邮件发送失败"
    
    

