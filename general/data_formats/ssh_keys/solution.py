import base64
import struct

with open("bruce_rsa_6e7ecd53b443a97013397b1a1ea30e14.pub", 'r') as f:
    pubkey_line = f.read().strip()

parts = pubkey_line.split()
base64_data = parts[1]
decoded_data = base64.b64decode(base64_data)

offset = 0
key_type_len = struct.unpack('>I', decoded_data[offset:offset+4])[0]
offset += 4 + key_type_len

exponent_len = struct.unpack('>I', decoded_data[offset:offset+4])[0]
offset += 4 + exponent_len

modulus_len = struct.unpack('>I', decoded_data[offset:offset+4])[0]
offset += 4
modulus_bytes = decoded_data[offset:offset+modulus_len]
modulus = int.from_bytes(modulus_bytes, byteorder='big')

print(modulus)
