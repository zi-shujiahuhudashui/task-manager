from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. 定义数据库地址。我们使用 SQLite，它会在本地生成一个 tasks.db 文件
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# 2. 创建数据库引擎。
# connect_args={"check_same_thread": False} 是 SQLite 的专属配置，为了让 FastAPI 多线程能访问
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 创建数据库会话工厂。以后每次操作数据库，都要找它开个“窗口”
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 创建基类。这是所有数据表（模型）的“老祖宗”
Base = declarative_base()