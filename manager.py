"""业务逻辑层：调度 storage，管理 Task 集合，用栈实现撤销。"""

import copy

import storage
from task import Task
from storage import JsonStorage


class TaskManager:
    def __init__(self, storage: JsonStorage):
        self.storage = storage
        # 从文件加载已有的任务
        self.tasks = self.storage.load()

        # 核心数据结构：撤销栈！
        # 栈里面装的是什么？是每一次操作之前的“任务列表快照”。
        # 比如要添加任务之前，先把当前的 self.tasks 复制一份压进栈里。
        self._undo_stack: list[list[Task]] = []

    def _snapshot(self) -> None:
        """
        内部私有方法：在每次修改状态前，把当前状态拍个快照存进栈里。
        提示：必须用 copy.deepcopy(self.tasks)，千万不能用 self.tasks.copy()！
        为什么？因为如果列表里装的是对象，浅拷贝（copy）只会复制地址，如果你修改了对象的属性，栈里的历史记录也会跟着变。必须深拷贝（deepcopy）。
        """
        # TODO: 实现压栈
        self._undo_stack.append(copy.deepcopy(self.tasks))



    def add_task(self, title: str, description: str = "") -> Task:
        """添加任务"""
        # TODO: 1. 调用 self._snapshot() 存快照
        # TODO: 2. 创建 Task 对象
        # TODO: 3. 加进 self.tasks 列表
        # TODO: 4. 调用 self.storage.save(self.tasks) 持久化
        # TODO: 5. 返回这个 Task 对象（方便 main.py 打印提示）
        self._snapshot()
        new_task = Task(title=title, description=description)
        self.tasks.append(new_task)
        self.storage.save(self.tasks)
        return new_task


    def list_tasks(self) -> list[Task]:
        """返回任务列表（只读）"""
        # 提示：为了防止外面的人拿到列表后瞎改（比如直接 pop 掉），最好返回一个浅拷贝 self.tasks.copy()
        # TODO: 实现
        task_copy=self.tasks.copy()
        return task_copy

    def complete_task(self, index: int) -> bool:
        """
        按序号（从 1 开始）标记完成。
        注意：传进来的 index 是用户看到的序号，在 Python 列表里应该是 index - 1。
        如果没找到，返回 False；成功返回 True。
        """
        # TODO: 1. 检查 index 是否越界（比如小于 1 或大于列表长度）
        # TODO: 2. 拿到任务对象，检查是否已经完成。如果已完成，直接 return False（不压栈）
        # TODO: 3. 调用 self._snapshot()
        # TODO: 4. 调用 task.mark_completed()
        # TODO: 5. 持久化保存
        # TODO: 6. return True
        if index < 1 or index > len(self.tasks):
            return False
        task = self.tasks[index-1]
        if task.completed:
            return False
        self._snapshot()
        task.mark_completed()
        self.storage.save(self.tasks)
        return True


    def uncomplete_task(self, index: int) -> bool:
        """取消完成（逻辑类似 complete_task，完成后要把 completed_at 设为 None）"""
        if index < 1 or index > len(self.tasks):
            return False
        task = self.tasks[index - 1]
        if not task.completed:
            return False
        self._snapshot()
        task.completed=False
        task.completed_at=None
        self.storage.save(self.tasks)
        return True

    def delete_task(self, index: int) -> bool:
        """删除任务"""
        # TODO: 自己写，逻辑类似 complete_task，核心是用 self.tasks.pop(index - 1)
        if index < 1 or index > len(self.tasks):
            return False
        self._snapshot()
        self.tasks.pop(index-1)
        self.storage.save(self.tasks)
        return True

    def undo(self) -> bool:
        """
        撤销操作。
        如果栈空了，返回 False。
        如果不空，从栈顶弹出一个快照，替换当前的 self.tasks，保存，并返回 True。
        """
        # 提示：用 self._undo_stack.pop() 拿出历史，赋值给 self.tasks
        # TODO: 实现
        if not self._undo_stack:
            return False
        self.tasks= self._undo_stack.pop()
        self.storage.save(self.tasks)
        return True

if __name__ == '__main__':
    test_file="data/test_manager.json"
    import os
    if os.path.exists(test_file):
        os.remove(test_file)
    print("---开始测试 TaskManager---")
    storage = JsonStorage(test_file)
    manager = TaskManager(storage)
    t1=manager.add_task("完成测试","test_manager")
    t2=manager.add_task("完成mian","任务管理器的mian")
    print(f"添加后当前的任务数：{len(manager.list_tasks())}")
    manager.complete_task(1)
    print(f"任务“完成测试”的状态：{manager.list_tasks()[0].completed}")
    manager.undo()
    print(f"撤销一次后，任务“完成测试”的完成状态：{manager.list_tasks()[0].completed}")
    manager.delete_task(2)
    print(f"删除任务“完成mian”,当前任务数{len(manager.list_tasks())}")
    manager.undo()
    print(f"撤销删除后，当前任务数：{len(manager.list_tasks())}")
    res=manager.complete_task(99)
    print(f"操作越界，返回res:{res}")
    print("--- 测试结束，如果所有数字都对，说明大管家逻辑完美！ ---")















