from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from uuid import uuid4
from .database import Base


class TaskModel(Base):
    # 定义数据库里的表名
    __tablename__ = "tasks"

    # 对应 v1 里的 id，用 UUID 自动生成
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))

    # 对应 v1 里的 title，不能为空
    title = Column(String, nullable=False)

    # 对应 v1 里的 description，默认为空字符串
    description = Column(String, default="")

    # 对应 v1 里的 completed，默认未完成
    completed = Column(Boolean, default=False)

    # 对应 v1 里的 created_at
    created_at = Column(DateTime, default=datetime.now)

    # 对应 v1 里的 completed_at，允许为空
    completed_at = Column(DateTime, nullable=True)