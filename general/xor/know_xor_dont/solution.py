from binascii import unhexlify

def xor_bytes(input, key):
    output = b''
    for b1, b2 in zip(input, key):
        output += bytes([b1 ^ b2])
    return output

data = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
cipher = unhexlify(data)

key_part = xor_bytes(cipher[:7], "crypto{".encode())
key = key_part + b"y"
key += key * int((len(cipher) - len(key)) / len(key))
key += key[:((len(cipher) - len(key)) % len(key))]

plain = xor_bytes(cipher, key).decode("utf-8")
print(plain)
