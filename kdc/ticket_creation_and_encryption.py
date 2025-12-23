import json
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_ticket(session_key, ticket_info):
    """
    Encrypt a ticket using AES-CBC with PKCS7 padding.
    Prepend IV to ciphertext for decryption.
    """
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(ticket_info.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def decrypt_ticket(session_key, ciphertext):
    """Decrypt a ticket using AES-CBC."""
    iv = ciphertext[:16]
    ct = ciphertext[16:]
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()

# Example ticket creation
ticket_info = json.dumps({"user": "alice", "timestamp": 1700000000})
encrypted_ticket = encrypt_ticket(session_key, ticket_info)
print("Encrypted ticket:", encrypted_ticket.hex())
