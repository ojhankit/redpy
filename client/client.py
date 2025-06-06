# client side code

import socket 
from config import HEADER, PORT, SERVER, ADDR, FORMAT, DISCONNECT_MESSAGE

ADDR = (SERVER,PORT)
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect(ADDR)

def send(message):
    message = message.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)

    send_length += b' ' * (HEADER - len(send_length))
    clientSocket.send(send_length)
    clientSocket.send(message)
    response = clientSocket.recv(2048).decode(FORMAT)
    print(f"[SERVER] {response}")

if __name__ == "__main__":
    print("[CONNECTED] You are connected to the server.")
    while True:

        message = input(">>>")
        if message.upper() == DISCONNECT_MESSAGE:
            send(DISCONNECT_MESSAGE)
            break
        send(message)
    
    print("[CLOSING] closing client")
    clientSocket.close()
    print("[CLOSED] client closed.")