from dotenv import load_dotenv
from pathlib import Path
import os
from .schema.mysql_schema import MySqlSchema
from langchain.tools import tool
import pymysql

# 加载环境变量
env_path = Path(__file__).parent.parent / "stu_agent.env"
load_dotenv(env_path)

# 定义工具
@tool("mysql_tool", args_schema=MySqlSchema)
def mysql_tool(sql:str) -> str:
    """
    执行mysql语句
    数据库模式：
    stu_agent.user_info 用户信息表：id,user_name,email
    stu_agent.sales_2024_07 销售记录表：
        id：自增主键
        order_date：记录销售发生的日期
        product_name：销售的具体产品名称
        category：产品所属类别（如电子产品、服装等）
        quantity：销售的产品数量
        unit_price：单个产品的价格
        total_amount：该笔销售的总金额（数量 × 单价）
        customer_city：购买客户所在的城市
    """
    try:
        # 连接数据库
        conn = pymysql.connect(
            host='localhost', 
            port=3306,
            user=os.getenv("MYSQL_USER"), 
            password=os.getenv("MYSQL_PASSWORD"), 
            db='stu_agent'
        )
        # 创建游标
        cursor = conn.cursor()
        # 执行SQL语句
        cursor.execute(sql)
        
        # 获取查询结果
        result = cursor.fetchall()
        
        # 提交事务
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        
        # 返回查询结果
        if result:
            print("SQL查询成功：", result)
            return str(result)
        else:
            return "SQL语句执行成功，但没有返回结果"
    except Exception as e:
        return f"执行SQL查询时出错: {e}"
