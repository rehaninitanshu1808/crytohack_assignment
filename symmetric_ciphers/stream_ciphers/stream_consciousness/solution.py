import subprocess
import json
from collections import Counter

BASE_URL = "https://aes.cryptohack.org/stream_consciousness"

def encrypt():
    result = subprocess.run(
        ["curl", "-s", f"{BASE_URL}/encrypt/"],
        capture_output=True,
        text=True
    )
    return bytes.fromhex(json.loads(result.stdout)['ciphertext'])

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

cts = []
for i in range(300):
    cts.append(encrypt())

flag_cts = [ct for ct in cts if len(ct) == 32]
flag_ct = flag_cts[0]

keystream = bytearray(xor(flag_ct[:7], b"crypto{"))

for pos in range(7, 32):
    votes = Counter()
    
    for ks_test in range(256):
        score = 0
        
        for ct in cts:
            if len(ct) > pos:
                pt_byte = ct[pos] ^ ks_test
                
                if pt_byte == 32:
                    score += 20
                elif pt_byte == 101:
                    score += 12
                elif pt_byte in b'taoinshrdlu':
                    score += 8
                elif 97 <= pt_byte <= 122:
                    score += 4
                elif 65 <= pt_byte <= 90:
                    score += 2
                elif pt_byte in b'.,!?_{}':
                    score += 3
                elif 48 <= pt_byte <= 57:
                    score += 2
                elif 32 <= pt_byte < 127:
                    score += 1
                else:
                    score -= 15
        
        votes[ks_test] = score
    
    best_ks = votes.most_common(1)[0][0]
    keystream.append(best_ks)

flag = xor(flag_ct, keystream)
print(flag.decode('ascii'))
