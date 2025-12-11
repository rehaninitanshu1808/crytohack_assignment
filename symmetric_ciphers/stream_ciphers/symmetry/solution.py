import subprocess
import json

BASE_URL = "https://aes.cryptohack.org/symmetry"

def encrypt(plaintext_hex, iv_hex):
    result = subprocess.run(
        ["curl", "-s", f"{BASE_URL}/encrypt/{plaintext_hex}/{iv_hex}/"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def encrypt_flag():
    result = subprocess.run(
        ["curl", "-s", f"{BASE_URL}/encrypt_flag/"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

response = encrypt_flag()
ciphertext_with_iv = response['ciphertext']
iv = ciphertext_with_iv[:32]
ciphertext = ciphertext_with_iv[32:]

response2 = encrypt(ciphertext, iv)
plaintext_hex = response2['ciphertext']
flag = bytes.fromhex(plaintext_hex).decode('utf-8')

print(flag)
