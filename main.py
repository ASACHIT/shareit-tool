import os
import socket
import threading

import cv2
import qrcode

banner = """
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
print(banner)


class Sharefile:
    def __init__(self, file_path: str, port: int = 8000):
        self.file_path = file_path
        self.port = port

    def create_qr_code(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        print("Generating Link 🔃")
        hosted_link = f"http://{self.ip}:{self.port}"
        print(hosted_link)
        print("Generating QR Code 🔃")
        qrcode_image = qrcode.make(hosted_link)
        qrcode_image.save("qrcode.png")

    def run_server(self):
        print("Getting Your Local Ip 🔃:", self.ip)
        print("Starting Local Server In Local Network 🔃")
        os.system(f"python -m http.server {self.port} --directory {self.file_path}")

    def show_qr(self):
        img_read = cv2.imread("qrcode.png")
        print("\n QR CODE SHOWN ✨|  SCAN 🔍 & OPEN URL 📎")
        cv2.imshow("Scan Qr code and Open Link ✨", img_read)
        cv2.waitKey(30000)
        cv2.destroyAllWindows()
        os.remove("qrcode.png")


# ------------------------------------------------------
def run():

    try:
        filepath = input("Input File or Folder Path 📂 To be Shared ~#")
        port = input("Input Port Number 🔢 Enter(Default:8000) ~#")
        object_ = Sharefile(file_path=filepath, port=port)
        object_.create_qr_code()
        t1 = threading.Thread(target=object_.show_qr)
        t2 = threading.Thread(target=object_.run_server)
        t1.start()
        t2.start()
    except KeyboardInterrupt:
        print("\n Thank You For Using")
        exit()


while __name__ == "__main__":
    run()
