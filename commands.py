import queue
from enum import Enum
import threading
from tasks import CompleteTask, Task


class CommandHandler:

    class KEYS(Enum):
        """
        Enum for the keys used in the command queue.
        """
        PRINT_ALLOCATED_PORTS = 1
        SHARE_FILE = 2

    def __init__(self, current_ports: list, task_queue: queue.Queue[Task], lock: threading.Lock):
        """
        Constructor for the CommandHandler class.
        :param current_ports: The list of ports currently allocated.
        :param task_queue: The task queue.
        :param lock: The lock.
        """
        self.current_ports = current_ports
        self.task_queue = task_queue
        self.lock = lock

    def print_allocated_ports(self):
        """
        Prints the list of ports currently allocated.
        """
        self.lock.acquire()
        for idx, port in enumerate(self.current_ports):
            print("{}. Allocated port: {}".format(idx, port))
        if len(self.current_ports) == 0:
            print("No ports allocated.")
        self.lock.release()

    def share_file(self):
        """
        Shares a file with the current allocated ports.
        """
        filepath = input("Enter the file path: ")
        port = int(input("Enter the port: "))
        self.task_queue.put(CompleteTask(filepath=filepath, lock=self.lock,
                                         task_queue=self.task_queue, port=port, current_ports=self.current_ports))

    def handle_command(self, command):
        """
        Handles the command.
        """
        if command == CommandHandler.KEYS.PRINT_ALLOCATED_PORTS.value:
            self.share_file()
        elif command == CommandHandler.KEYS.SHARE_FILE.value:
            self.print_allocated_ports()

    @staticmethod
    def help():
        """
        Prints the help message.
        """
        print("What do you want to do?")
        print("1. Share file")
        print("2. Print allocated ports")
        print("3. Exit")
