import hashlib
import json
import re

from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')


get_params = lambda r: json.loads(re.findall(b"{.*}", r.recvline())[0])
r = remote("socket.cryptohack.org", 13373)
params = {**get_params(r), **get_params(r), **get_params(r)}

# Sending A as g to Bob, we get A^b = (g^a)^b = g^(a*b) which is our shared secret
r.sendline(json.dumps({'p': params['p'], 'g': params['A'], 'A': hex(0xd3adbeef)}))
new_params = {**get_params(r), **get_params(r)}

print(decrypt_flag(int(new_params['B'], 16), params['iv'], params['encrypted']))
