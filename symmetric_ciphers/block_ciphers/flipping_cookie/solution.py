import subprocess
import json

BASE_URL = "https://aes.cryptohack.org/flipping_cookie"

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def get_cookie():
    result = subprocess.run(
        ["curl", "-s", f"{BASE_URL}/get_cookie/"],
        capture_output=True,
        text=True
    )
    cookie_hex = json.loads(result.stdout)['cookie']
    cookie_bytes = bytes.fromhex(cookie_hex)
    return cookie_bytes[:16], cookie_bytes[16:]

def check_admin(cookie_hex, iv_hex):
    result = subprocess.run(
        ["curl", "-s", f"{BASE_URL}/check_admin/{cookie_hex}/{iv_hex}/"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

iv, ciphertext = get_cookie()
original_plaintext = b"admin=False;expi"
target_plaintext = b"admin=True;expir"
xor_diff = xor_bytes(original_plaintext, target_plaintext)
modified_iv = xor_bytes(iv, xor_diff)
response = check_admin(ciphertext.hex(), modified_iv.hex())

print(response['flag'])
