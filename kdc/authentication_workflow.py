import time

# In-memory user database: username -> secret key
USER_DB = {
    "alice": os.urandom(16),
    "bob": os.urandom(16)
}

def authenticate_user(username, user_secret):
    """
    Authenticate a user and issue a session key ticket.
    Returns session key and encrypted ticket if successful.
    """
    if username not in USER_DB or USER_DB[username] != user_secret:
        return None

    session_key = generate_session_key()
    timestamp = int(time.time())
    ticket_data = json.dumps({
        "username": username,
        "session_key": session_key.hex(),
        "timestamp": timestamp
    })

    encrypted_ticket = encrypt_ticket(user_secret, ticket_data)
    return {
        "session_key": session_key,
        "ticket": encrypted_ticket
    }

# Example usage
alice_secret = USER_DB["alice"]
auth_response = authenticate_user("alice", alice_secret)

if auth_response:
    print("Ticket issued to Alice:", auth_response["ticket"].hex())
    decrypted_ticket = decrypt_ticket(alice_secret, auth_response["ticket"])
    print("Decrypted ticket content:", decrypted_ticket)
else:
    print("Authentication failed.")
