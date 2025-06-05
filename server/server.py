import time
import threading
import socket
from config import HEADER,PORT,SERVER,DISCONNECT_MESSAGE,FORMAT


isServerRunning = True
ADDR = (SERVER,PORT)

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(ADDR)

def handle_client(conn, addr):

    print(f"[NEW CONNECTION] {addr} connected")

    isConnected = True
    while isConnected:

        try:
            message_length = conn.recv(HEADER).decode(FORMAT)
            try:
                message_length = int(message_length.strip())
                message = conn.recv(message_length).decode(FORMAT)

                if message == DISCONNECT_MESSAGE:
                    isConnected = False
                
                print(f"[{addr}] : {message}")
                conn.send(f"Server Received: {message}".encode(FORMAT))

            except Exception as e:
                print(f"Exception occured {e}")
        except Exception as e:
            print("Exception occured in making connection : {e}")
            break
    
    conn.close()
    print(f"[DISCONNECCTED]   {addr}")

def start():

    serverSocket.listen()
    print(f"[LISTENING] server is listening on {SERVER}:{PORT}")
    
    while isServerRunning:

        conn ,addr = serverSocket.accept()
        thread = threading.Thread(target=handle_client,
                                  args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":

    print("[STARTING] Server is starting..")
    start()

