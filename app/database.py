from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. 告诉程序：我们要用 SQLite 数据库，文件名叫 tasks.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# 2. 启动引擎。connect_args 是 SQLite 专属的特权配置
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 这是数据库的“会话工厂”。以后每次要查数据，就开个窗口
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 创建一个基类。以后我们所有的表，都要继承它
Base = declarative_base()