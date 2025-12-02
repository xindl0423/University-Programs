import socket
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

host = 'localhost'
port = 1000

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

print("Server is running and waiting for message")

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((host,port))
    s.listen()
    conn,addr = s.accept()
    with conn:
        print('Connected with',addr)

        encoded_message = conn.recv(256)
        encoded_signature = conn.recv(256)

        message = private_key.decrypt(encoded_message,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

    with open("client_public.pem","rb") as f:
            client_public = serialization.load_pem_public_key(f.read())

    try:
        client_public.verify(
            encoded_signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        print("Signature verified ")
    except Exception:
        print("Signature verification failed ")

    print(f"Decrypted message: {message.decode()}")