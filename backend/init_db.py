from app.database.session import engine, Base
from app.entity import db_models

print("开始创建数据库表...")
Base.metadata.create_all(bind=engine)
print("所有表创建完成！")
