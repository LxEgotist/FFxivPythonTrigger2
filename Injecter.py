import pymem
import sys
import os
from json import dumps
import _thread
import socket
import time

print(sys.version)

pm = pymem.Pymem('ffxiv_dx11.exe')
pm.inject_python_interpreter()

wdir = os.path.abspath('.')
log_path = os.path.join(wdir, 'out.log').replace("\\", "\\\\")
err_path = os.path.join(wdir, 'err.log').replace("\\", "\\\\")
shellcode1 = """
import sys
from os import chdir
from traceback import format_exc
try:
    sys.path=%s
    chdir(sys.path[0])
    exec(open("%s").read())
except:
    with open("%s", "w+") as f:
        f.write(format_exc())
""" % (
    dumps(sys.path),
    'Entrance.py',
    err_path
)
_thread.start_new_thread(pm.inject_python_shellcode, tuple([shellcode1]))

print("loading...")
HOST, PORT = "127.0.0.1", 3520
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        sock.connect((HOST, PORT))
        break
    except:
        time.sleep(1)
print("connect!")
while True:
    size = int.from_bytes(sock.recv(4), 'little',signed=True)
    if size < 0:
        break
    else:
        print(sock.recv(size).decode('utf-8'))
