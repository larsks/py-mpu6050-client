import cStringIO as StringIO
import json
import select
import six
import socket
import time
import zmq

class ZMQClient(object):
    def __init__(self, src):
        self.src = src
        self.init_zmq()
        self.init_socket()

    def init_zmq(self):
        self.ctx = zmq.Context()

    def init_socket(self):
        self.socket = self.ctx.socket(zmq.SUB)
        self.socket.setsockopt(
            zmq.SUBSCRIBE,
            six.binary_type(''))

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        self.socket.connect(self.src)
        while True:
            data = json.loads(self.socket.recv())
            return dict(zip(
                ['yaw', 'pitch', 'roll', 'temp'],
                data))

class SocketClient(object):
    def __init__(self, src, blksize=8192):
        self.src = src
        self.blksize = blksize

        self._values = self.values()

    def __iter__(self):
        return self._values

    def __next__(self):
        return self.next()

    def next(self):
        return next(self._values)

    def values(self):
        while True:
            print 'connecting to {}'.format(self.src)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(self.src)
            except socket.error as exc:
                print 'error {} connecting to socket; retrying...'.format(exc)
                time.sleep(1)
                continue

            for value in self.clientloop(sock):
                yield value

            sock.close()
            time.sleep(1)

    def clientloop(self, sock):
        poll = select.poll()
        poll.register(sock, select.POLLIN|select.POLLHUP)

        buf = ''
        lastread = time.time()

        while True:
            ready = poll.poll(1000)
            if not ready and (time.time() - lastread > 2):
                break

            for obj, event in ready:
                if event & select.POLLHUP:
                    return
                elif event & select.POLLIN:
                    lastread=time.time()
                    data = sock.recv(self.blksize)
                    buf += data

                    while '\n' in buf:
                        line, buf = buf.split('\n', 1)
                        vals = json.loads(line)
                        yield vals