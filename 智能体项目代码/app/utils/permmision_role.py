from langchain.tools import tool
from app.ai.schema.mysqlscheme import MysqlScheme
from dotenv import load_dotenv
import os
import pymysql
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)

load_dotenv()


def permission_role(user_id:str) -> str:
    sql = f"SELECT role FROM user_info WHERE user_email='{user_id}'"


    try:
        con = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PAW"),
            database=os.getenv("MYSQL_DATABASE")
        )
        cursor = con.cursor()
        cursor.execute(sql)

        result = cursor.fetchall()
        # print(result)
        if len(result) > 0:
            return result[0][0]
        else:
            return None

    except Exception as e:
        logger.warning("MySQL 执行失败")
        return "执行失败"


if __name__ == "__main__":
    rs = permission_role("3327354636@qq.com")
    print(rs)

    