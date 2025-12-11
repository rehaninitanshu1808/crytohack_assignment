import json
import socket

HOST = "socket.cryptohack.org"
PORT = 13399

def send_command(s, option, **kwargs):
    cmd = {"option": option}
    cmd.update(kwargs)
    s.sendall((json.dumps(cmd) + '\n').encode())
    response = s.recv(4096).decode()
    return json.loads(response)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.recv(4096)
    
    token_hex = "00" * 28
    
    for attempt in range(1, 1001):
        send_command(s, "reset_connection")
        send_command(s, "reset_password", token=token_hex)
        result = send_command(s, "authenticate", password="")
        
        if "flag" in result.get('msg', '').lower():
            print(result['msg'])
            break
