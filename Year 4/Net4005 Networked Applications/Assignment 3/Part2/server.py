import socket, os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import secrets

host = 'localhost'
port = 1002

if not os.path.exists('server_private.pem'):
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    with open('server_private.pem','wb') as f:
        f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()))
    with open('server_public.pem','wb') as f:
        f.write(private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo))
else :
    with open('server_private.pem','rb') as f:
        private_key = serialization.load_pem_private_key(f.read(),password=None)


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((host,port))
    s.listen()
    print("Server is running and waiting for message")
    conn,addr = s.accept()
    with conn:
        print('Connected with',addr)

        encoded_aes= conn.recv(256)
        aes_key = private_key.decrypt(
            encoded_aes,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)
        )

        while True:
            nonce = conn.recv(16)
            ciphertext = conn.recv(4096)
            decryptor = Cipher(algorithms.AES(aes_key), modes.CTR(nonce), backend=default_backend()).decryptor()
            message = decryptor.update(ciphertext) + decryptor.finalize()
            print("Client:", message.decode())

            reply = input("Enter message (or quit)\n")
            if reply == 'quit':
                break
            nonce2 = secrets.token_bytes(16)
            reply = reply.encode()
            encryptor = Cipher(algorithms.AES(aes_key),modes.CTR(nonce2), backend=default_backend()).encryptor()
            cipher_text = encryptor.update(reply) +  encryptor.finalize()
            conn.sendall(nonce2 + cipher_text)
