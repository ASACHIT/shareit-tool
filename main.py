import os
import time
import queue
import subprocess
import socket
import threading
from qrcode import QRCode
from abc import ABC, abstractmethod


class Task(ABC):
    @abstractmethod
    def run(self):
        pass


task_queue: queue.Queue[Task] = queue.Queue()


current_ports = []

lock = threading.Lock()


class TaskQueue(threading.Thread):
    def __init__(self, task_queue: queue.Queue[Task]):
        threading.Thread.__init__(self)
        self.task_queue = task_queue

    def run(self):
        while True:
            next_task = self.task_queue.get()
            next_task.run()
            self.task_queue.task_done()


class SpawnPythonServerTask(Task):
    def __init__(self, port, dir_):
        self.port = port
        self.dir_ = dir_

    def run(self):
        lock.acquire()
        current_ports.append({"port": self.port, "dir": self.dir_})
        lock.release()

        subprocess.Popen(
            "python3 -m http.server {} --directory {}".format(self.port, self.dir_).split(" "))


class CreateQRCodeTask(Task):
    def __init__(self, text, file_name):
        self.text = text
        self.file_name = file_name

    def run(self):
        qrcode = QRCode()
        print(self.text)
        qrcode.add_data(self.text)
        print("\n\n")
        qrcode.print_tty()
        print("\n\n")


class CompleteTask(Task):

    def __init__(self, filepath: str, port: int,  task_queue: queue.Queue[Task]):
        self.task_queue = task_queue
        self.filepath = filepath
        self.port = port

    def run(self):
        self.task_queue.put(SpawnPythonServerTask(self.port, self.filepath))
        ip = socket.gethostbyname(socket.gethostname())
        self.task_queue.put(CreateQRCodeTask(
            "http://{}:{}".format(ip, self.port), f"{self.port}-qrcode.png"))


if __name__ == "__main__":
    BANNER = """
    *****************************************************
    *    ____  _   _    _    ____  _____   ___ _____    *
    *   / ___|| | | |  / \  |  _ \| ____| |_ _|_   _|   *
    *   \___ \| |_| | / _ \ | |_) |  _|    | |  | |     *
    *    ___) |  _  |/ ___ \|  _ <| |___   | |  | |     *
    *   |____/|_| |_/_/   \_\_| \_\_____| |___| |_|.py  *
    *                                                   *
    *   Programmed By Sachit Yadav                      *
    *   https://github.com/ASACHIT/shareit-tool.git     *
    *****************************************************
    """

    print(BANNER)

    try:
        thread_pool = []
        for i in range(5):
            taskDaemon = TaskQueue(task_queue)
            taskDaemon.daemon = True
            taskDaemon.start()

        while True:
            print("What do you want to do?")
            print("1. Share a file.")
            print("2. Print currently shared files.")
            print("3. Exit.")

            choice = int(input("Enter your choice: "))

            if choice == 1:
                filepath = input("Enter the file path: ")
                port = int(input("Enter the port: "))
                task_queue.put(CompleteTask(filepath, port, task_queue))
                time.sleep(2)
            elif choice == 2:
                lock.acquire()
                print(current_ports)
                lock.release()
            elif choice == 3:
                break
            else:
                print("Invalid choice.")


    except KeyboardInterrupt:
        print("IDK How to Handle this.")
