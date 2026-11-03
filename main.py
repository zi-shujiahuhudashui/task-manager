"""命令行入口层。只负责输入输出和调用 Manager。"""
import sys
from manager import TaskManager
from storage import JsonStorage, StorageError

def print_task_list(tasks):
    if not tasks:
        print("当前没有任何任务")
    else:
        print("-" * 30)
        for i, t in enumerate(tasks, start=1):
            status = "[√]" if t.completed else "[ ]"
            print(f"{i}. {t.title} {status}")
            if t.description:
                print(f"       备注: {t.description}")
        print("-" * 30)
def main():
    # 1. 初始化仓库和大管家
    storage = JsonStorage()
    manager = TaskManager(storage)

    print("欢迎使用 Task Manager！输入 'help' 查看指令。")

    # 2. 永远在循环里等待用户输入
    while True:
        try:
            # 接收用户输入，并去掉首尾空格
            command_line = input("\n> ").strip()
            if not command_line:
                continue

            # 将输入按空格切分。比如 "add 买牛奶" 变成 ["add", "买牛奶"]
            # split把字符串切成一个列表，maxsplit=1，意思是“最多只切一刀
            parts = command_line.split(maxsplit=1)
            # .lower()：是字符串（String）自带的内置方法，能把字母全变成小写。
            # 这样用户无论输入ADD、Add还是add，程序都能认出来
            cmd = parts[0].lower()  # 比如 "add"
            arg = parts[1] if len(parts) > 1 else ""

            if cmd == "help":
                print("\n可用指令：")
                print("  add <标题> <备注/形容>     添加新任务 (add 标题 备注/形容(可选)) 例如：add 买牛奶 去超市")
                print("  list           查看所有任务")
                print("  done <序号>    标记任务为完成 例如：done 1")
                print("  undone <序号>  取消任务完成状态 例如：undone 1")
                print("  del <序号>     删除任务 例如：del 1")
                print("  undo           撤销上一次操作")
                print("  quit           退出程序")
                print("注意:add,done undone,del操作时指令和序号要有空格输入")
                continue
            # 3. 根据命令分发
            if cmd == "add":
                if not arg:
                    print("错误：请输入任务标题！")
                    continue
                title_list=arg.split(maxsplit=1)
                title = title_list[0]
                description = title_list[1] if len(title_list) > 1 else ""
                task = manager.add_task(title, description)
                print(f"成功添加任务 任务名：[{task.title}]，任务备注/形容：[{task.description}]")
                print_task_list(manager.list_tasks())

            elif cmd == "list":
                tasks = manager.list_tasks()
                if not tasks:
                    print("当前没有任何任务")
                else:
                    print("-" * 30)
                    for i, t in enumerate(tasks, start=1):
                        status = "[√]" if t.completed else "[ ]"
                        print(f"{i}. {t.title} {status}")
                    print("-" * 30)

            elif cmd == "done":
                # 提示：判断 arg 能不能转成整数，然后调 manager.complete_task()
                if not arg.isdigit():
                    print("错误：请输入正确的任务序号（纯数字）")
                    continue
                index = int(arg)
                if manager.complete_task(index):
                    print(f"序号为 {index} 的任务已标为‘已完成’")
                else:
                    print(f"操作失败：序号为 {index} 的任务不存在，或者已经完成了")
                print_task_list(manager.list_tasks())

            elif cmd == "undone":
                # 提示：类似 done，调 manager.uncomplete_task()
                if not arg.isdigit():
                    print("错误：请输入正确的任务序号（纯数字）")
                    continue
                index = int(arg)
                if manager.uncomplete_task(index):
                    print(f"序号为 {index} 的任务已标为未完成")
                else:
                    print(f"操作失败：序号为 {index} 的任务不存在，或者已经标为‘未完成’")
                print_task_list(manager.list_tasks())

            elif cmd == "del":
                # 提示：类似 done，调 manager.delete_task()
                if not arg.isdigit():
                    print("错误：请输入正确的任务序号（纯数字）")
                    continue
                index = int(arg)
                if manager.delete_task(index):
                    print(f"序号为 {index} 的任务已删除")
                else:
                    print(f"操作失败：序号为 {index} 的任务不存在")
                print_task_list(manager.list_tasks())

            elif cmd == "undo":
                # 提示：调 manager.undo()
                if manager.undo():
                    print("已撤销一次更改")
                else:
                    print("已撤销至原始状态")
                print_task_list(manager.list_tasks())

            elif cmd == "quit":
                print("再见！")
                break

            else:
                print("未知指令，请输入 help 查看帮助。")

        except StorageError as e:
            print(f"【系统错误】{e}")
        except Exception as e:
            print(f"【发生异常】{e}")
        except KeyboardInterrupt:
            # 捕获用户按 Ctrl+C 的情况
            print("\n再见！")
            break


if __name__ == "__main__":
    main()