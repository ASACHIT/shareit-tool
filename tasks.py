import threading
import subprocess
import socket
import queue
from qrcode import QRCode
from abc import ABC, abstractmethod

class Task(ABC):
    @abstractmethod
    def run(self):
        """
        This method is called when the task is started.
        """
        pass

class TaskQueue(threading.Thread):
    def __init__(self, task_queue: queue.Queue[Task]):
        """
        Initializes the task queue.
        """
        threading.Thread.__init__(self)
        self.task_queue = task_queue

    def run(self):
        """
        Runs the task queue.
        """
        while True:
            next_task = self.task_queue.get()
            next_task.run()
            self.task_queue.task_done()


class SpawnPythonServerTask(Task):
    def __init__(self, port, dir_, lock, current_ports):
        """
        Initializes the task of spawning a python server..
        """
        self.port = port
        self.dir_ = dir_
        self.lock = lock
        self.current_ports = current_ports

    def run(self):
        """
        Runs the task of spawning a python server.
        """
        self.lock.acquire()
        self.current_ports.append({"port": self.port, "dir": self.dir_})
        self.lock.release()

        subprocess.Popen(
            "python3 -m http.server {} --directory {}".format(self.port, self.dir_).split(" "))


class CreateQRCodeTask(Task):
    def __init__(self, text, file_name):
        """
        Initializes the task of creating a qr code.
        """
        self.text = text
        self.file_name = file_name

    def run(self):
        """
        Runs the task of creating a qr code.
        """
        qrcode = QRCode()
        qrcode.add_data(self.text)
        qrcode.print_tty()


class CompleteTask(Task):

    def __init__(self, filepath: str, port: int, lock: threading.Lock,  task_queue: queue.Queue[Task], current_ports: list):
        """
        Initializes the complete task.
        """
        self.task_queue = task_queue
        self.filepath = filepath
        self.port = port
        self.lock = lock
        self.current_ports = current_ports

    def run(self):
        """
        Runs the complete task.
        """
        self.task_queue.put(SpawnPythonServerTask(self.port, self.filepath, self.lock, self.current_ports))
        ip = socket.gethostbyname(socket.gethostname())
        self.task_queue.put(CreateQRCodeTask(
            "http://{}:{}".format(ip, self.port), f"{self.port}-qrcode.png"))
