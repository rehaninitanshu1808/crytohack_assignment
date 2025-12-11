import socket
import json

HOST = "socket.cryptohack.org"
PORT = 13421

def send_command(s, option, **kwargs):
    cmd = {"option": option}
    cmd.update(kwargs)
    s.sendall((json.dumps(cmd) + '\n').encode())
    response = s.recv(4096).decode()
    return json.loads(response)

def has_valid_padding(s, iv, ct):
    test = (iv + ct).hex()
    response = send_command(s, "unpad", ct=test)
    return response.get("result", False)

def decrypt_block(s, ct_block, prev_block):
    intermediate = bytearray(16)
    
    for pad_len in range(1, 17):
        byte_index = 16 - pad_len
        fake_iv = bytearray(16)
        
        for i in range(byte_index + 1, 16):
            fake_iv[i] = intermediate[i] ^ pad_len
        
        candidates = []
        for guess in range(256):
            fake_iv[byte_index] = guess
            if has_valid_padding(s, bytes(fake_iv), ct_block):
                candidates.append(guess)
        
        if len(candidates) == 1 or pad_len > 1:
            intermediate[byte_index] = candidates[0] ^ pad_len
        else:
            for guess in candidates:
                fake_iv[byte_index] = guess
                fake_iv2 = bytearray(fake_iv)
                fake_iv2[14] = (fake_iv[14] + 1) % 256
                
                if not has_valid_padding(s, bytes(fake_iv2), ct_block):
                    intermediate[byte_index] = guess ^ pad_len
                    break
    
    return bytes(intermediate[i] ^ prev_block[i] for i in range(16))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.recv(4096)
    
    response = send_command(s, "encrypt")
    full_ct = bytes.fromhex(response['ct'])
    
    iv = full_ct[:16]
    ct = full_ct[16:]
    
    ct_blocks = [ct[i*16:(i+1)*16] for i in range(len(ct) // 16)]
    plaintext_blocks = []
    
    for i, ct_block in enumerate(ct_blocks):
        prev_block = iv if i == 0 else ct_blocks[i-1]
        plaintext_blocks.append(decrypt_block(s, ct_block, prev_block))
    
    plaintext = b''.join(plaintext_blocks)
    
    pad_len = plaintext[-1]
    if 1 <= pad_len <= 16 and all(b == pad_len for b in plaintext[-pad_len:]):
        plaintext = plaintext[:-pad_len]
    
    message = plaintext.decode('ascii')
    response = send_command(s, "check", message=message)
    
    print(response['flag'])
