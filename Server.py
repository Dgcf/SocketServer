import socket
import time
import threading
import json
import collections


HOST = '127.0.0.1'
PORT = 50007
THREAD_NUM = 100
BUF_SIZE = 1024


class ClientSocket(threading.Thread):
    """
    一个客户端一个ClientSocket，负责收发数据
    """
    def __init__(self, sock, address, name='client'):
        threading.Thread.__init__(self)
        self._sock = sock
        self._address = address
        self._name = name
        self._msg_deque = collections.deque(maxlen=10)
        self.send_message = SendThread(self.sock, self._address, self._msg_deque)
        self.send_message.start()

    def run(self):
        while True:
            msg = self._sock.recv(BUF_SIZE)
            self._msg_deque.append(ClientMessage(msg))


class SendThread(threading.Thread):
    """
    一个ClientSocket用来发送数据
    """
    def __init__(self, sock, address, msg, name='send_thread'):
        self._sock = sock
        self._address = address
        self._name = name
        self._msg = msg

    def run(self):
        while True:
            try:
                send_msg = self._msg.popleft().msg
            except IndexError:
                continue
            print("send message")
            self._sock.sendall(send_msg)


class ClientMessage:
    """
    序列化和反序列化接收到的数据
    """
    def __init__(self, msg):
        self._msg = msg

    @property
    def msg(self):
        return self._serialize()

    def _deserialize(self):
        try:
            self._msg = json.loads(self._msg.decode())
            try:
                if self._msg['type'] == 'login':
                    if self._msg['content'] == '123':
                        self._msg['content'] = 'true'
            except KeyError:
                print('msg has not type key')
        except json.JSONDecodeError:
            print('json decoder fail')

    def _serialize(self):
        self.deserialize()
        return json.dumps(self._msg.encode())


if __name__ == '__main__':
    threads = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(THREAD_NUM)
        while True:
            print('wait accept client...')
            conn, address = sock.accept()
            send_thread = ClientSocket(conn, address)
            threads.append(send_thread)

