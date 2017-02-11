import json
import select
import socket
import time

class SocketClient(object):
    def __init__(self, src, blksize=1024):
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
                sock = socket.create_connection(self.src, timeout=10)
                print 'connected!'
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

        while True:
            ready = poll.poll(2000)
            if not ready:
                break

            for obj, event in ready:
                if event & select.POLLHUP:
                    return
                elif event & select.POLLIN:
                    data = sock.recv(self.blksize)
                    buf += data

                    while '\n' in buf:
                        line, buf = buf.split('\n', 1)
                        vals = json.loads(line)
                        yield vals
