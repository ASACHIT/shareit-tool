import queue
import threading
import time

from commands import CommandHandler
from tasks import Task, TaskQueue
from constants import BANNER

TASK_QUEUE: queue.Queue[Task] = queue.Queue()
CURR_PORTS = []
THREAD_POOL: list[threading.Thread] = []
LOCK = threading.Lock()


def initialize_thread_pool():
    """
    Initialize the thread pool.
    """
    for i in range(5):
        taskDaemon = TaskQueue(TASK_QUEUE)
        taskDaemon.daemon = True
        taskDaemon.start()
        THREAD_POOL.append(taskDaemon)


if __name__ == "__main__":
    try:

        print(BANNER)
        initialize_thread_pool()

        commandHandler = CommandHandler(CURR_PORTS, TASK_QUEUE, LOCK)

        while True:
            CommandHandler.help()
            choice = int(input("Enter your choice: "))
            commandHandler.handle_command(choice)
            time.sleep(1)

    except KeyboardInterrupt:
        print("IDK How to Handle this.")
