import subprocess
import json

def encrypt(pt_hex, key_hex):
    result = subprocess.run(
        ["curl", "-s", f"http://aes.cryptohack.org/triple_des/encrypt/{key_hex}/{pt_hex}/"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)['ciphertext']

def encrypt_flag(key_hex):
    result = subprocess.run(
        ["curl", "-s", f"http://aes.cryptohack.org/triple_des/encrypt_flag/{key_hex}/"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)['ciphertext']

key = (b'\x00'*8 + b'\xff'*8).hex()
ct_flag = encrypt_flag(key)
ct = encrypt(ct_flag, key)

print(bytes.fromhex(ct).decode())
