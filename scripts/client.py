#!/usr/bin/env python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 2369))
s.sendall('hello'.encode())
s.close()