import json

from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

starter = b"a" * 16
p = remote('socket.cryptohack.org', 13388)
p.recvline()
p.sendline(json.dumps({"option": "sign", "message": starter.hex()}))
response = json.loads(p.recvline().decode())
signature = bytes.fromhex(response['signature'])
wanted = pad(b"admin=True", 16)
newhash = bxor(AES.new(wanted, AES.MODE_ECB).encrypt(signature), signature)
newmessage = pad(starter, 16) + b"admin=True"
p.sendline(json.dumps({"option": "get_flag", "message": newmessage.hex(), "signature": newhash.hex()}))
print(p.recvline())
