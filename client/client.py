# client side code
import sys
import os
import socket 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

ADDR = (config.SERVER,config.PORT)
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect(ADDR)

def send(message):
    message = message.encode(config.FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(config.FORMAT)

    send_length += b' ' * (config.HEADER - len(send_length))
    clientSocket.send(send_length)
    clientSocket.send(message)
    response = clientSocket.recv(2048).decode(config.FORMAT)
    print(f"[SERVER] {response}")

if __name__ == "__main__":
    print("[CONNECTED] You are connected to the server.")
    while True:

        message = input(">>>")
        if message.upper() == config.DISCONNECT_MESSAGE:
            send(config.DISCONNECT_MESSAGE)
            break
        send(message)
    
    print("[CLOSING] closing client")
    clientSocket.close()
    print("[CLOSED] client closed.")