import json
import socket

doc1 = "4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2"
doc2 = "4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2"

HOST = "socket.cryptohack.org"
PORT = 13389

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.recv(1024)
    s.sendall(json.dumps({"document": doc1}).encode() + b'\n')
    s.recv(1024)
    s.sendall(json.dumps({"document": doc2}).encode() + b'\n')
    print(s.recv(1024).decode())

