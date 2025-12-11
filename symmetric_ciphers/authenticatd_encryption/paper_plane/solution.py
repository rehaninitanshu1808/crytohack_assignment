import subprocess
import json

BASE_URL = "https://aes.cryptohack.org/paper_plane/"

def encrypt_flag():
    result = subprocess.run(
        ["curl", "-s", BASE_URL + "encrypt_flag/"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def send_msg(ciphertext_hex, m0_hex, c0_hex):
    url = f"{BASE_URL}send_msg/{ciphertext_hex}/{m0_hex}/{c0_hex}/"
    result = subprocess.run(
        ["curl", "-s", url],
        capture_output=True, text=True
    )
    try:
        return json.loads(result.stdout)
    except:
        return {"error": "parse"}

def has_valid_padding(ct_hex, m0_hex, c0_hex):
    result = send_msg(ct_hex, m0_hex, c0_hex)
    return "Message received" in result.get("msg", "")

def padding_oracle_attack_single_block(block, m0_fixed):
    I = bytearray(16)
    
    for byte_pos in range(15, -1, -1):
        pad_len = 16 - byte_pos
        target_pad = pad_len
        
        c0_test = bytearray(16)
        for j in range(byte_pos + 1, 16):
            c0_test[j] = I[j] ^ target_pad
        
        for val in range(256):
            c0_test[byte_pos] = val
            
            if has_valid_padding(block.hex(), m0_fixed.hex(), bytes(c0_test).hex()):
                I[byte_pos] = target_pad ^ val
                break
    
    return bytes(I)

data = encrypt_flag()
ct = bytes.fromhex(data['ciphertext'])
m0_orig = bytes.fromhex(data['m0'])
c0_orig = bytes.fromhex(data['c0'])

C1 = ct[0:16]
C2 = ct[16:32]

I1 = padding_oracle_attack_single_block(C1, m0_orig)
P1 = bytes(I1[i] ^ c0_orig[i] for i in range(16))

I2 = padding_oracle_attack_single_block(C2, P1)
P2 = bytes(I2[i] ^ C1[i] for i in range(16))

plaintext = P1 + P2
if plaintext and plaintext[-1] <= 16:
    pad_len = plaintext[-1]
    if all(b == pad_len for b in plaintext[-pad_len:]):
        plaintext = plaintext[:-pad_len]

print(plaintext.decode('ascii'))
