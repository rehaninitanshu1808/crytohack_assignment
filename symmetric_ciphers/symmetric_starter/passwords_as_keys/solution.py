import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

ciphertext = bytes.fromhex("c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66")

with open('/usr/share/dict/words', 'r') as f:
    words = [w.strip() for w in f.readlines()]

for word in words:
    key = hashlib.md5(word.encode()).digest()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    try:
        plaintext_str = plaintext.decode('utf-8')
        if plaintext_str.startswith('crypto{'):
            print(plaintext_str)
            break
    except:
        pass
