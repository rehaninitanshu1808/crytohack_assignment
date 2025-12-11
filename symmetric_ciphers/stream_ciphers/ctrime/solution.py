import subprocess
import json
import string

BASE_URL = "https://aes.cryptohack.org/ctrime"

def encrypt(pt_bytes):
    result = subprocess.run(
        ["curl", "-s", f"{BASE_URL}/encrypt/{pt_bytes.hex()}/"],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)
    return len(data['ciphertext'])

flag = b'crypto{'
charset = (string.ascii_letters + string.digits + '_{!}@#$%^&*()-=+[]').encode()

while not flag.endswith(b'}'):
    best_char = None
    best_length = float('inf')
    
    for char_byte in charset:
        candidate = flag + bytes([char_byte])
        test = candidate + candidate
        length = encrypt(test)
        
        if length < best_length:
            best_length = length
            best_char = char_byte
    
    flag += bytes([best_char])
    
    if len(flag) > 100:
        break

print(flag.decode())
