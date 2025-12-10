import hashlib
import json
from socket import socket

import sympy
from Crypto.Cipher import AES


sock = socket()
sock.connect(("socket.cryptohack.org", 13379))

buf = b""


def recvline():
    global buf
    while b'\n' not in buf:
        buf += sock.recv(4096)
    idx = buf.index(b'\n') + 1
    line = buf[:idx].decode('utf-8')
    buf = buf[idx:]
    return line.strip()


def recvuntil(marker):
    global buf
    marker_bytes = marker.encode('utf-8')
    while marker_bytes not in buf:
        buf += sock.recv(4096)
    idx = buf.index(marker_bytes) + len(marker_bytes)
    data = buf[:idx]
    buf = buf[idx:]
    return data.decode('utf-8')


def sendline(data):
    sock.send((data + '\n').encode('utf-8'))


recv_alice = lambda: json.loads(recvuntil('Intercepted from Alice: ').split(': ')[-1] + recvline())
recv_bob = lambda: json.loads(recvuntil('Intercepted from Bob: ').split(': ')[-1] + recvline())

send_alice = lambda payload: (recvuntil('Send to Alice: '), sendline(json.dumps(payload)))
send_bob = lambda payload: (recvuntil('Send to Bob: '), sendline(json.dumps(payload)))

msg = recv_alice()
send_bob({'supported': ['DH64']})

msg = recv_bob()
assert msg['chosen'] == 'DH64'
send_alice(msg)

msg = recv_alice()
p, g, A = (int(msg[x][2:], 16) for x in 'pgA')

msg = recv_bob()
B = int(msg['B'][2:], 16)

msg = recv_alice()
iv = bytes.fromhex(msg['iv'])
enc_flag = bytes.fromhex(msg['encrypted_flag'])

# Compute discrete log - fast since we restricted p to 64 bits
a = sympy.ntheory.residue_ntheory.discrete_log(p, A, g)

shared_secret = pow(B, a, p)
key = hashlib.sha1(str(shared_secret).encode('ascii')).digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv)

print(cipher.decrypt(enc_flag))
