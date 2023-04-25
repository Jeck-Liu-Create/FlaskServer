import multiprocessing
import socket
import threading
import time
class TCPclient:
    def __init__(self):
        self.queue = multiprocessing.Queue() # TCP发送队列
        self.sleep_time = 0

    def queue_wirte(self,senddata):
        print("队列写入")
        self.queue.put(senddata)

    def queue_read(self):
        if not self.queue.empty():
            value = self.queue.get()
            print("get %s from Queue", value)
            return value

    def tcp_client(self):
        global client
        print("首次TCP 客户端打开")
        connect = False
        while True:
            try:
                if connect == False:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.settimeout(5)
                    client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)
                    client.connect(("10.18.23.115", 5001))
                    connect = True
                if not self.queue.empty():
                    returndata = self.queue_read()
                    print("回复电文")
                    print(returndata)
                    client.send(returndata)
                    recv_data = client.recv(1024)
                    print(recv_data.decode('utf-8'))
                else:
                    time.sleep(0.01)
            except socket.error as e:
                print("Address-related error connecting to server: %s" % e)
                print("请等待重新连接Level2服务器")
                connect = False

    def add_heartbeat(self):
        senddata = bytes('12', 'ASCII')
        while True :
            time.sleep(1)
            self.sleep_time += 1
            if (self.sleep_time == 10):
                self.queue_wirte(senddata)
                print(senddata)
                self.sleep_time = 0

if __name__ == "__main__":
    one=TCPclient()
    clinet_thread = threading.Thread(target=one.tcp_client)
    heardbeat_thread = threading.Thread(target=one.add_heartbeat)
    clinet_thread.start()
    heardbeat_thread.start()
