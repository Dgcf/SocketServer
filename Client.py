import socket
import time


HOST = '127.0.0.1'
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:
        s = input("please input: ")
        print("start send, time: ", time.ctime())
        sock.sendall(bytes(s, 'utf-8'))
        data = sock.recv(1024)
        print("accept: ", data)
