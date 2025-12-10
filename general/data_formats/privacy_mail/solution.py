from Crypto.PublicKey import RSA

with open('privacy_enhanced_mail.pem', 'r') as f:
    key_data = f.read()

key = RSA.importKey(key_data)
d = key.d

print(d)
