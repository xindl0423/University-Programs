import socket
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

host = 'localhost'
port = 1000

if not os.path.exists('client_private.pem'):
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    with open('client_private.pem','wb') as f:
        f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()))
    with open('client_public.pem','wb') as f:
        f.write(private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo))
else :
    with open('client_private.pem','rb') as f:
        private_key = serialization.load_pem_private_key(f.read(),password=None)

with open('server_public.pem','rb') as f:
        server_key = serialization.load_pem_public_key(f.read())

message = input('Enter the message: ').encode()

encoded_message = server_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((host,port))
    s.sendall(encoded_message)
    s.sendall(signature)