import socket
import time
import threading


HOST = '127.0.0.1'
PORT = 50007
THREAD_NUM = 100


def thread_fun(sock):
    conn, addr = sock.accept()
    with conn:
        print('conn', conn)
        print('connected by', addr[0], addr[1])
        while True:
            print(time.ctime())
            data = conn.recv(1024)
            print(data)
            if data == b'0':
                break
            conn.sendall(data.upper())


class SocketThread(threading.Thread):
    def __init__(self, func, args, name='new thread'):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        self.func(*self.args)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(THREAD_NUM)
    threads = []
    for i in range(10):
        threads.append(SocketThread(thread_fun, sock))

    for i in range(10):
        threads[i].start()

    for i in range(10):
        threads[i].join()
