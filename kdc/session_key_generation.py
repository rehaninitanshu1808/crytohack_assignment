import os

def generate_session_key():
    """
    Generate a cryptographically secure 16-byte session key.
    Each session key is unique and short-lived.
    """
    return os.urandom(16)

# Example usage
session_key = generate_session_key()
print("Generated session key (hex):", session_key.hex())
