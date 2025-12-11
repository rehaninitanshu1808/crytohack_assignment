import sys
import os
from chacha20 import ChaCha20

def bytes_to_words(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]

def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

def word(x):
    return x % (2 ** 32)

def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w])

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def rotate_inv(x, n):
    return rotate(x, 32 - n)

def quarter_round_inverse(x, a, b, c, d):
    x[b] = rotate_inv(x[b], 7); x[b] ^= x[c]; x[c] = word(x[c] - x[d])
    x[d] = rotate_inv(x[d], 8); x[d] ^= x[a]; x[a] = word(x[a] - x[b])
    x[b] = rotate_inv(x[b], 12); x[b] ^= x[c]; x[c] = word(x[c] - x[d])
    x[d] = rotate_inv(x[d], 16); x[d] ^= x[a]; x[a] = word(x[a] - x[b])

def inner_block_inverse(state):
    quarter_round_inverse(state, 3, 4, 9, 14)
    quarter_round_inverse(state, 2, 7, 8, 13)
    quarter_round_inverse(state, 1, 6, 11, 12)
    quarter_round_inverse(state, 0, 5, 10, 15)
    quarter_round_inverse(state, 3, 7, 11, 15)
    quarter_round_inverse(state, 2, 6, 10, 14)
    quarter_round_inverse(state, 1, 5, 9, 13)
    quarter_round_inverse(state, 0, 4, 8, 12)

iv1 = bytes.fromhex('e42758d6d218013ea63e3c49')
iv2 = bytes.fromhex('a99f9a7d097daabd2aa2a235')
msg_enc = bytes.fromhex('f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f')
flag_enc = bytes.fromhex('b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732')
msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'

keystream1 = xor(msg, msg_enc)
state_after_rounds = bytes_to_words(keystream1[:64])

state = state_after_rounds.copy()
for i in range(10):
    inner_block_inverse(state)

key_words = state[4:12]
key = words_to_bytes(key_words)

c = ChaCha20()
flag = c.decrypt(flag_enc, key, iv2)

print(flag.decode('ascii'))
