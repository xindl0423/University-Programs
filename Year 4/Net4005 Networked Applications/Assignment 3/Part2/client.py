import socket, os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import secrets

host = 'localhost'
port = 1002

with open('server_public.pem','rb') as f:
    server_public_key = serialization.load_pem_public_key(f.read())

aes_key = secrets.token_bytes(32)
encrypted_aes_key = server_public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((host,port))
    s.sendall(encrypted_aes_key)
    while True:
        message = input("Enter message (or quit)\n")
        if message == 'quit':
            break
        message = message.encode()
        nonce = secrets.token_bytes(16)
        encryptor = Cipher(algorithms.AES(aes_key), modes.CTR(nonce), backend=default_backend()).encryptor()
        cipher_text = encryptor.update(message) + encryptor.finalize()
        s.sendall(nonce + cipher_text)

        nonce2 = s.recv(16)
        ciphertext_reply = s.recv(4096)
        decryptor = Cipher(algorithms.AES(aes_key), modes.CTR(nonce2), backend=default_backend()).decryptor()
        response = decryptor.update(ciphertext_reply) + decryptor.finalize()
        print("Server reply:",response.decode())
