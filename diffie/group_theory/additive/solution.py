import hashlib
import json

from pwn import remote
from Crypto.Cipher import AES
from Crypto.Util.number import inverse
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


r = remote("socket.cryptohack.org", 13380)
A_data = json.loads(r.recvline().decode().strip().split("Alice: ")[1])
B_data = json.loads(r.recvline().decode().strip().split("Bob: ")[1])
flag = json.loads(r.recvline().decode().strip().split("Alice: ")[1])
print(flag)

p = int(A_data["p"], 0)
g = int(A_data["g"], 0)
A = int(A_data["A"], 0)
B = int(B_data["B"], 0)

a_priv = A * inverse(2, p) % p
shared = B * a_priv % p

print(decrypt_flag(shared, flag['iv'], flag['encrypted']))