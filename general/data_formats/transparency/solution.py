import hashlib
from Crypto.PublicKey import RSA

pem = open('transparency.pem', 'r').read()
key = RSA.importKey(pem).public_key()
der = key.exportKey(format='DER')
sha256_fingerprint = hashlib.sha256(der).hexdigest()

print(sha256_fingerprint)
