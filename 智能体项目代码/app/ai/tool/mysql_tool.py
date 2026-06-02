from langchain.tools import tool
from app.ai.schema.mysqlscheme import MysqlScheme
from dotenv import load_dotenv
import os
import pymysql
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)

load_dotenv()

@tool("mysql_tool",args_schema=MysqlScheme)
def mysql_tool(sql: str) -> str:
    """
    执行 MySQL 语句，支持读写操作。
    读操作（SELECT/SHOW/DESCRIBE/EXPLAIN）返回查询结果；
    写操作（INSERT/UPDATE/DELETE/其他 DDL/DML）执行提交并返回影响行数。
    user_info 表结构如下：nser_id,user_name,user_email

    orders（订单表） 表结构如下：
        order_id：订单 ID
        user_id：用户 ID
        order_date：下单日期
        product_id：商品 ID
        quantity：购买数量
        total_amount：订单总金额
        payment_method：支付方式
        order_status：订单状态
    products（商品表） 表结构如下：
        product_id：商品 ID
        product_name：商品名称
        category：商品分类
        price：商品单价
        stock：库存数量
        sales_volume：销量
        average_rating：平均评分
    sales（销售统计表） 表结构如下：
        year：年月
        total_sales：销售总额
        total_orders：订单总数
        total_quantity_sold：销售总数量
        category：商品分类
        average_order_value：平均订单金额
    user_behavior（用户行为表） 表结构如下：
        user_id：用户 ID
        product_id：商品 ID
        action：用户行为（浏览 / 收藏 / 购买）
        action_date：行为发生日期
        device：使用设备
    users（用户表）表结构如下：
        user_id：用户 ID
        username：用户名
        registration_date：注册日期
        country：国家
        age：年龄
        gender：性别
        total_spent：累计消费金额
        order_count：订单数量

    """
    con = None
    cursor = None
    try:
        con = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PAW"),
            database=os.getenv("MYSQL_DATABASE")
        )
        cursor = con.cursor()
        sql_text = sql.strip()
        cursor.execute(sql_text)

        if sql_text.lower().startswith(("select", "show", "describe", "explain")):
            result = cursor.fetchall()
            return str(result)

        con.commit()
        return f"写入成功，影响行数：{cursor.rowcount}"

    except Exception as e:
        logger.warning(f"MySQL 执行失败：{e}")
        return f"执行失败：{e}"
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()
