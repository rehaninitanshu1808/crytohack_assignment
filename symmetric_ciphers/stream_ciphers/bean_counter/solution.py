import subprocess
import json

BASE_URL = "https://aes.cryptohack.org/bean_counter"
PNG_HEADER = bytes.fromhex('89504e470d0a1a0a0000000d49484452')

def encrypt():
    result = subprocess.run(
        ["curl", "-s", f"{BASE_URL}/encrypt/"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

response = encrypt()
encrypted_bytes = bytes.fromhex(response['encrypted'])

first_ciphertext_block = encrypted_bytes[:16]
keystream = bytes(c ^ p for c, p in zip(first_ciphertext_block, PNG_HEADER))

decrypted = bytearray()
for i in range(0, len(encrypted_bytes), 16):
    block = encrypted_bytes[i:i+16]
    decrypted_block = bytes(c ^ k for c, k in zip(block, keystream[:len(block)]))
    decrypted.extend(decrypted_block)

with open('flag.png', 'wb') as f:
    f.write(decrypted)
