"""任务数据模型。只负责：Task 长什么样，怎么和 dict 互转。"""

# field 用于给类的属性设置更复杂的默认值。
from dataclasses import dataclass, field
from datetime import datetime  # 处理时间
from typing import Optional    # 类型提示
from uuid import uuid4         # 生成不重复的随机字符串


# dataclass 是个装饰器，能自动帮我们生成初始化方法（__init__）等。
@dataclass
class Task:
    title: str
    description: str = ""   # 描述必须是个字符串，如果不传，默认是空字符串 ""
    completed: bool = False # 默认是未完成，非常合理
    id: str = field(default_factory=lambda: str(uuid4()))
    # 创建时间
    created_at: datetime = field(default_factory=datetime.now)
    # Optional[datetime] 的意思是：这个变量要么是一个 datetime 对象，要么是 None（空）。
    # 完成时间
    completed_at: Optional[datetime] = None

    # 定义一个方法，把当前的对象转成字典。
    def to_dict(self) -> dict:
        # TODO: 你来实现
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            # 把 datetime 对象变成字符串
            # self.created_at 是个 datetime 对象，不能直接进 JSON。
            # .isoformat() 把它转成类似 "2026-10-31T12:00:00" 的字符串。
            "created_at": self.created_at.isoformat(),
            # 如果 completed_at 有值，就转字符串；如果没有（None），就保持 None
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

    # 定义一个方法，把当前的字符串转成对象。
    # @classmethod意思是这是类的方法，不是单个对象的方法
    # @classmethod 是类方法。它不需要对象实例（t1）来调用，直接用 Task.from_dict() 就能调用。
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        # 如果 created_at_str 有值，就把它从字符串转回 datetime 对象；
        # 如果是空的（比如你手贱删了它），就默认用当前时间 datetime.now()。
        created_at_str = data.get("created_at")
        created_at = datetime.fromisoformat(created_at_str) if created_at_str else datetime.now()

        completed_at_str = data.get("completed_at")
        completed_at = datetime.fromisoformat(completed_at_str) if completed_at_str else None

        # 2. 组装成一个全新的 Task 并返回
        # cls(...) 等同于 Task(...)
        return cls(
            # data.get("id", 默认值)：尝试获取 id，如果没有，就生成一个新的 uuid4。
            id=data.get("id", str(uuid4())),
            title=data.get("title", ""),
            description=data.get("description", ""),
            completed=data.get("completed", False),
            created_at=created_at,
            completed_at=completed_at
        )

    # 标记任务完成的动作
    def mark_completed(self) -> None:
        # TODO: 你来实现
        # 如果已经是完成状态，直接返回，不刷新完成时间
        if self.completed:
            return

        # 标记为完成，并记录当前时间
        self.completed = True
        self.completed_at = datetime.now()


# 这是 Python 的一个特殊魔法。
# 意思是：如果当前这个文件被直接运行（而不是被别的文件 import），下面的代码才会执行。
if __name__ == "__main__":
    print("--- 测试开始 ---")
    # 1. 创建一个任务
    t1 = Task(title="买牛奶", description="去超市买两盒")
    print(f"原始任务: {t1}")

    # 2. 测试 to_dict (对象转字典)
    d = t1.to_dict()
    print(f"转成字典 (准备存文件): {d}")

    # 3. 测试 from_dict (字典转对象)
    t2 = Task.from_dict(d)
    print(f"从字典恢复 (从文件读出): {t2}")
    # assert 叫“断言”，用来测试。如果 t1.id 不等于 t2.id，程序会直接崩溃并抛出后面的错误文字。
    assert t1.id == t2.id, "报错：重建后 ID 变了"

    # 4. 测试标记完成
    t1.mark_completed()
    print(f"完成一次后: completed={t1.completed}, 完成时间={t1.completed_at}")

    # 5. 测试重复标记完成 (时间不能被刷新)
    old_time = t1.completed_at
    t1.mark_completed()
    assert t1.completed_at == old_time, "报错：重复完成导致时间被刷新了"
    print("重复完成测试通过，时间没变。")

    print("--- 所有测试通过！地基很稳！ ---")