import json

from pwn import *

HOST = "socket.cryptohack.org"
PORT = 13405

msg_A_bytes = b'A' * 31
msg_B_bytes = b'A' * 31 + b'\x01'

payload = {
    "m1": msg_A_bytes.hex(),
    "m2": msg_B_bytes.hex()
}

r = remote(HOST, PORT)
r.sendline(json.dumps(payload).encode())
print(r.recvall().decode())
r.close()
