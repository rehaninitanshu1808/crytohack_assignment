import requests

BASE_URL = "http://aes.cryptohack.org/block_cipher_starter"

r = requests.get(f"{BASE_URL}/encrypt_flag")
ciphertext = r.json()["ciphertext"]

r = requests.get(f"{BASE_URL}/decrypt/{ciphertext}")
plaintext = r.json()["plaintext"]

print(bytearray.fromhex(plaintext).decode())
