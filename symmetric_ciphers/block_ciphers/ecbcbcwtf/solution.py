import subprocess
import json

CBC_CIPHERTEXT = "6a7d306b25f649b22500f00b55cf54ea3ae74da57413a81acc01a3565f5ef2cde09779c16fd432ab69893cd4a53826ec"

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

cbc_bytes = bytes.fromhex(CBC_CIPHERTEXT)
block_size = 16
iv = cbc_bytes[:block_size]
ciphertext_blocks = [cbc_bytes[i:i+block_size] for i in range(block_size, len(cbc_bytes), block_size)]

decrypted_blocks = []
for block in ciphertext_blocks:
    result = subprocess.run(
        ["curl", "-s", f"https://aes.cryptohack.org/ecbcbcwtf/decrypt/{block.hex()}/"],
        capture_output=True,
        text=True
    )
    decrypted = bytes.fromhex(json.loads(result.stdout)['plaintext'])
    decrypted_blocks.append(decrypted)

plaintext_blocks = []
p1 = xor_bytes(decrypted_blocks[0], iv)
plaintext_blocks.append(p1)

for i in range(1, len(decrypted_blocks)):
    pi = xor_bytes(decrypted_blocks[i], ciphertext_blocks[i-1])
    plaintext_blocks.append(pi)

plaintext = b''.join(plaintext_blocks)
print(plaintext.decode('utf-8'))
