from pydantic import BaseModel,Field

class MysqlScheme(BaseModel):
    sql:str=Field(...,description="mysql语句")