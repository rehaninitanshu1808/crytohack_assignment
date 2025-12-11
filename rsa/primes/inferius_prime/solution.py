from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes
p, q = 752708788837165590355094155871, 986369682585281993933185289261
n, phi = p * q, (p - 1) * (q - 1)
e = 3
d = inverse(e, phi)
ct = 39207274348578481322317340648475596807303160111338236677373
print(long_to_bytes(pow(ct, d, n)))