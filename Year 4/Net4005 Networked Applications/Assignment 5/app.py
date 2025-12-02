from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    ip_addr = request.remote_addr
    return f"<h1>You are connecting from {ip_addr}</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port = 8080)