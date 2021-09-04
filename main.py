import os
import socket
import threading

import cv2
import qrcode


class Sharefile:
    def __init__(self, file_path: str, port: int = 8000):
        self.file_path = file_path
        self.port = port

    def create_qr_code(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        print("Generating Link...")
        if self.port == "":
            self.port = 8000
        hosted_link = f"http://{self.ip}:{self.port}"
        print(hosted_link)
        print("Generating QR Code...")
        qrcode_image = qrcode.make(hosted_link)
        print("Saving Generated Qr Code...")
        qrcode_image.save("qrcode.png")

    def run_server(self):
        print("Getting Your Local Ip:", self.ip)
        print("Hosting Local Server in Local Network !")
        os.system(
            f"python -m http.server {self.port} --directory {self.file_path}")

    def show_qr(self):
        print("Reading Qr Code...")
        img_read = cv2.imread("qrcode.png")
        print("Displaying QR CODE | Scan It Before it get Losts !!")
        cv2.imshow("Scan Qr code and Open Link", img_read)
        cv2.waitKey(20000)
        cv2.destroyAllWindows()
        os.system("del qrcode.png")


# _-------------------------------------------------------
def run():
    filepath = input("Input File or Folder Path To be Shared ~# ")
    port = input("Input Port Number Enter(Default:8000) ~# ")
    object_ = Sharefile(file_path=filepath, port=port)
    object_.create_qr_code()
    t1 = threading.Thread(target=object_.show_qr)
    t2 = threading.Thread(target=object_.run_server)
    t1.start()
    t2.start()
    t2.join()
    t1.join()


run()
