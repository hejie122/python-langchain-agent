from langchain.tools import tool
from app.ai.schema.emailscheme import EmailScheme
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)

load_dotenv()


@tool("send_email",args_schema=EmailScheme)
def send_email(to:str,subject:str,content:str) -> str:
    """
    发送邮件
    """
    try:
        msg=MIMEText(content)

        msg["to"]=to
        msg["from"]=os.getenv("FROM_EMAIL")
        msg["Subject"]=subject
        smtp=smtplib.SMTP_SSL(host=os.getenv("UEL_EMAIL"),port=465)
        smtp.login(user=os.getenv("FROM_EMAIL"),password=os.getenv("PAW_EMAIL"))
        smtp.sendmail(from_addr=os.getenv("FROM_EMAIL"),to_addrs=to,msg=msg.as_string())
        logger.info("邮件发送成功")
        return "发送成功"
    except Exception as e:
        logger.debug(f"邮件发送失败：{e}")
        return "发送失败"