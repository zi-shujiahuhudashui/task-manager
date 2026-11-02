"""JSON 持久化层（基础版）。只负责读写，不需要高级语法。"""
import json
import os
from task import Task

class StorageError(Exception):
    """存储出错时抛出这个异常"""
    pass

class JsonStorage:
    def __init__(self, file_path: str = "data/tasks.json"):
        # 就用普通的字符串存路径
        self.file_path = file_path

    def load(self) -> list[Task]:
        # 如果文件不存在，返回空列表
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 把读出来的字典，变成 Task 对象
            return [Task.from_dict(item) for item in data]
        except Exception as e:
            raise StorageError(f"读取文件坏了: {e}")

    def save(self, tasks: list[Task]) -> None:
        # os.makedirs 用于创建文件夹。
        # 如果程序第一次运行，电脑里没有 data 这个文件夹，这句代码会帮你建一个。
        # exist_ok=True 意思是：如果 data 文件夹已经存在了，别报错，假装无事发生。
        os.makedirs("data", exist_ok=True)

        # 把对象变成字典
        data = [t.to_dict() for t in tasks]

        try:
            # 直接写文件
            with open(self.file_path, "w", encoding="utf-8") as f:
                # json.dump 是 dump（倾倒）的意思，把 Python 的列表，倒进文件 f 里。
                # ensure_ascii=False：如果不加这个，你的中文“买牛奶”会被存成
                # "\u4e70\u725b\u5976"，加上它就能正常显示中文。
                # indent=2：让你的 JSON 文件自动换行并缩进 2 个空格，打开看的时候非常整齐漂亮。
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise StorageError(f"保存失败: {e}")


if __name__ == "__main__":
    # 测试代码，随便写个路径比如 test_data.json
    storage = JsonStorage("data/test_data.json")

    # 1. 测试空文件加载
    print("加载初始状态:", storage.load())

    # 2. 测试保存
    t1 = Task(title="测试持久化")
    t2 = Task(title="测试保存")
    storage.save([t1, t2])
    print("保存成功！去左侧看看有没有生成 data 文件夹")

    # 3. 测试加载
    loaded = storage.load()
    print("读取出的任务数量:", len(loaded))
    print("读取的内容:", loaded)