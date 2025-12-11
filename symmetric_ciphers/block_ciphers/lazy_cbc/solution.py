import subprocess
import json

BASE_URL = "https://aes.cryptohack.org/lazy_cbc"

def api_call(endpoint, param):
    result = subprocess.run(
        ["curl", "-s", f"{BASE_URL}/{endpoint}/{param}/"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def encrypt(plaintext_hex):
    return api_call("encrypt", plaintext_hex)

def receive(ciphertext_hex):
    return api_call("receive", ciphertext_hex)

def get_flag(key_hex):
    return api_call("get_flag", key_hex)

plaintext = b'\x00' * 16
response = encrypt(plaintext.hex())
C1 = bytes.fromhex(response['ciphertext'])

attack_ciphertext = b'\x00' * 16 + C1
response = receive(attack_ciphertext.hex())

plaintext_hex = response['error'].split(': ')[1]
plaintext_bytes = bytes.fromhex(plaintext_hex)
recovered_key = plaintext_bytes[16:32]

flag_response = get_flag(recovered_key.hex())
flag = bytes.fromhex(flag_response['plaintext']).decode()

print(flag)
