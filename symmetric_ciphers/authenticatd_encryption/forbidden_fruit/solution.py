import json
import urllib.request
import ssl

BASE_URL = "https://aes.cryptohack.org/forbidden_fruit/"
ssl_context = ssl._create_unverified_context()

def encrypt(plaintext_hex):
    url = f"{BASE_URL}encrypt/{plaintext_hex}/"
    with urllib.request.urlopen(url, context=ssl_context) as response:
        return json.loads(response.read().decode('utf-8'))

def decrypt(nonce_hex, ciphertext_hex, tag_hex, ad_hex):
    url = f"{BASE_URL}decrypt/{nonce_hex}/{ciphertext_hex}/{tag_hex}/{ad_hex}/"
    with urllib.request.urlopen(url, context=ssl_context) as response:
        return json.loads(response.read().decode('utf-8'))

def bytes_to_poly(b):
    """Convert bytes to polynomial (GCM uses big-endian)."""
    return int.from_bytes(b, 'big')

def poly_to_bytes(p):
    """Convert polynomial to bytes."""
    return p.to_bytes(16, 'big')

def gf_mult(x, y):
    """Multiply in GF(2^128) with reduction poly x^128 + x^7 + x^2 + x + 1."""
    z = 0
    v = x
    for i in range(128):
        if y & (1 << (127 - i)):
            z ^= v
        if v & 1:
            v = (v >> 1) ^ (0xe1 << 120)
        else:
            v >>= 1
    return z

def ghash(h, ad, c):
    """Compute GHASH."""
    ad_padded = ad + b'\x00' * ((16 - len(ad) % 16) % 16)
    c_padded = c + b'\x00' * ((16 - len(c) % 16) % 16)
    
    blocks = []
    for i in range(0, len(ad_padded), 16):
        blocks.append(bytes_to_poly(ad_padded[i:i+16]))
    for i in range(0, len(c_padded), 16):
        blocks.append(bytes_to_poly(c_padded[i:i+16]))
    
    len_block = (len(ad) * 8 << 64) | (len(c) * 8)
    blocks.append(len_block)
    
    y = 0
    for block in blocks:
        y = gf_mult(y ^ block, h)
    
    return y

AD = b"CryptoHack"

enc1 = encrypt("41" * 16)
enc2 = encrypt("42" * 16)

nonce = bytes.fromhex(enc1['nonce'])
c1 = bytes.fromhex(enc1['ciphertext'])
t1 = bytes_to_poly(bytes.fromhex(enc1['tag']))
c2 = bytes.fromhex(enc2['ciphertext'])
t2 = bytes_to_poly(bytes.fromhex(enc2['tag']))

c1_poly = bytes_to_poly(c1)
c2_poly = bytes_to_poly(c2)

# Recover H: H^2 = (T1 XOR T2) / (C1 XOR C2)
t_diff = t1 ^ t2
c_diff = c1_poly ^ c2_poly

# Inverse in GF(2^128): x^(-1) = x^(2^128 - 2)
c_diff_inv = c_diff
for _ in range(126):
    c_diff_inv = gf_mult(c_diff_inv, c_diff_inv)
    c_diff_inv = gf_mult(c_diff_inv, c_diff)
c_diff_inv = gf_mult(c_diff_inv, c_diff_inv)

h_squared = gf_mult(t_diff, c_diff_inv)

# Square root: sqrt(x) = x^(2^127)
h = h_squared
for _ in range(127):
    h = gf_mult(h, h)

# Verify and get S (try both roots)
for h_candidate in [h, h ^ (1 << 127)]:
    gh1 = ghash(h_candidate, AD, c1)
    s = t1 ^ gh1
    
    gh2 = ghash(h_candidate, AD, c2)
    if (gh2 ^ s) == t2:
        h = h_candidate
        break
else:
    print("Failed to verify H")
    exit(1)

# Forge tag
target = b"give me the flag"
enc_target = encrypt(target.hex())
ct_target = bytes.fromhex(enc_target['ciphertext'])

gh_target = ghash(h, AD, ct_target)
tag_forged = poly_to_bytes(gh_target ^ s)

result = decrypt(nonce.hex(), ct_target.hex(), tag_forged.hex(), AD.hex())

if "plaintext" in result:
    print(bytes.fromhex(result['plaintext']).decode('ascii'))
else:
    print(f"Error: {result}")
