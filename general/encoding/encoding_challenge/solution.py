from pwn import *
import json
import base64
import codecs
from binascii import unhexlify

r = remote('socket.cryptohack.org', 13377)

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def list_to_string(s):
    return "".join(s)

for i in range(101):
    received = json_recv()
    if "flag" in received:
        print(received["flag"])
        break

    word = received["encoded"]
    encoding = received["type"]

    if encoding == "base64":
        decoded = base64.b64decode(word).decode('utf8').replace("'", '"')
    elif encoding == "hex":
        decoded = unhexlify(word).decode('utf8').replace("'", '"')
    elif encoding == "rot13":
        decoded = codecs.decode(word, 'rot_13')
    elif encoding == "bigint":
        decoded = unhexlify(word.replace("0x", "")).decode('utf8').replace("'", '"')
    elif encoding == "utf-8":
        decoded = list_to_string([chr(b) for b in word])

    json_send({"decoded": decoded})
