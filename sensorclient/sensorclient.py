import json
import select
import socket
import time

default_port = 8000
default_listen_addr = '0.0.0.0'
default_blksize = 1024

def sensorclient(listen_addr=default_listen_addr,
                 port=default_port,
                 blksize=default_blksize):
        print 'listening for data on {}:{}'.format(listen_addr, port)
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((listen_addr, port))
            buf = ''
            poll = select.poll()
            poll.register(sock, select.POLLIN)
            vals = [[0,0,0]] * 3

            while True:
                ready = poll.poll(10)

                # in the absence of any new data, continue to yield
                # the last value to client code.  This prevents the
                # vispy UI from blocking.
                if not ready:
                    yield vals
                    continue

                data, saddr = sock.recvfrom(blksize)
                buf += data

                while '\n' in buf:
                    line, buf = buf.split('\n', 1)
                    vals = json.loads(line)
                    yield vals

            sock.close()
