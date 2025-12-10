import hashlib
from json import loads, dumps

from pwn import remote
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import getPrime
from sympy.ntheory.residue_ntheory import discrete_log
from gmpy2 import is_prime


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


def getParams():
    Alice = loads(io.recvline().split(b":", 1)[1])
    Bob = loads(io.recvline().split(b":", 1)[1])
    cipher = loads(io.recvline().split(b":", 1)[1])
    iv = cipher['iv']
    encrypted = cipher['encrypted']
    return Alice, Bob, iv, encrypted


def getSmoothP(p, digits):
    pSmooth = 2
    primes = []
    while pSmooth.bit_length() < p.bit_length():
        prime = getPrime(digits)
        if prime not in primes:
            pSmooth *= prime
            primes.append(prime)
    pSmooth += 1
    return pSmooth


io = remote("socket.cryptohack.org", 13378)
Alice, Bob, iv, encrypted = getParams()

p = int(Alice["p"], 16)
pSmooth = 0
while not is_prime(pSmooth):
    pSmooth = getSmoothP(p, 32)

print("Smooth prime is", pSmooth)
print("Iv is", iv)
print("encrypted is", encrypted)

io.sendline(dumps({"p": hex(pSmooth), "g": Alice["g"], "A": Alice["A"]}))
reply = loads(io.recvline().split(b":", 2)[2])
B = int(reply["B"], 16)

b = discrete_log(pSmooth, B, 2)
print("Reused key of Bob found --->", b)
shared_secret = pow(int(Alice['A'], 16), b, p)
print(decrypt_flag(shared_secret, iv, encrypted))
