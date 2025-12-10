from cryptography import x509
from cryptography.hazmat.backends import default_backend

with open("2048b-rsa-example-cert_3220bd92e30015fe4fbeb84a755e7ca5.der", 'rb') as f:
    der_data = f.read()

cert = x509.load_der_x509_certificate(der_data, default_backend())
public_key = cert.public_key()
modulus = public_key.public_numbers().n

print(modulus)
