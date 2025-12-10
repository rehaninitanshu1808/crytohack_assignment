from binascii import unhexlify

def single_byte_xor(input, key):
    output = b''
    for b in input:
        output += bytes([b ^ key])
    try:
        return output.decode("utf-8")
    except:
        return None

data = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
decoded = unhexlify(data)

for i in range(256):
    result = single_byte_xor(decoded, i)
    if result and "crypto" in result:
        print(result)
        break
