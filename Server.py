import socket
import time


HOST = '127.0.0.1'
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    with conn:
        print('connected by', addr)
        while True:
            print(time.ctime())
            data = conn.recv(1024)
            print(data)
            if data == b'0':
                break
            conn.sendall(data.upper())
