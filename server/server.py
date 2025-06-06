#import time
import threading
import socket
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from commands.parser import parse_commands



isServerRunning = True
ADDR = (config.SERVER,config.PORT)

client_threads = {}

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    isConnected = True
    while isConnected:

        try:
            message_length = conn.recv(config.HEADER).decode(config.FORMAT)
            try:
                message_length = int(message_length.strip())
                message = conn.recv(message_length).decode(config.FORMAT)

                if message == config.DISCONNECT_MESSAGE:
                    isConnected = False
                
                print(f"[{addr}] : {message}")
                response = parse_commands(message)
                #conn.send(f"Server Received: {message}".
                # encode(config.FORMAT))
                conn.send(response.encode(config.FORMAT))

            except Exception as e:
                print(f"Exception occured {e}")
        except Exception as e:
            print("Exception occured in making connection : {e}")
            break
    
    conn.close()
    print(f"[DISCONNECCTED]   {addr}")

"""
def start():

    serverSocket.listen()
    print(f"[LISTENING] server is listening on {SERVER}:{PORT}")
    
    while isServerRunning:

        conn ,addr = serverSocket.accept()
        thread = threading.Thread(target=handle_client,
                                  args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
"""

def accept_connection():
    serverSocket.listen()
    print(f"[LISTENING] Server is listening on {config.SERVER}:{config.PORT}")

    while isServerRunning:
        try:
            serverSocket.settimeout(1.0) # prevent blocking
            conn,addr = serverSocket.accept()
            thread = threading.Thread(target=handle_client,
                                      args=(conn,addr))
            thread.start()
            client_threads.append(thread)
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
        except socket.timeout:
            continue
        except OSError:
            break

if __name__ == "__main__":

    print("[STARTING] Server is starting..")
    accept_thread = threading.Thread(target=accept_connection)
    accept_thread.start()

    while True:
        cmd = input()
        if cmd.lower() == "exit":
            print("[SHUTTING DOWN] Closing server...")
            server_running = False
            serverSocket.close()
            break

    
    accept_thread.join()

    for t in client_threads:
        t.join()
    
    print("[SERVER STOPPED]")
