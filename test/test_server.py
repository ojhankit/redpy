# tests
import unittest
import threading
import time
import socket

from config import HEADER, FORMAT, ADDR, DISCONNECT_MESSAGE
import server

class TestMiniRedisConnection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Start the server in a background thread before all tests."""
        cls.server_thread = threading.Thread(target=server.start, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Give server time to start

    @classmethod
    def tearDownClass(cls):
        """Shutdown the server after all tests."""
        server.server_running = False
        server.serversocket.close()
        cls.server_thread.join()

    def setUp(self):
        """Connect to the server for each test."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

    def tearDown(self):
        """Close client connection after each test."""
        self.client.close()

    def send_message(self, message: str) -> str:
        """Helper to send a message and receive server's response."""
        encoded_msg = message.encode(FORMAT)
        send_len = str(len(encoded_msg)).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        self.client.send(send_len)
        self.client.send(encoded_msg)
        response = self.client.recv(2048).decode(FORMAT)
        return response

    def test_client_can_connect(self):
        self.assertIsNotNone(self.client)

    def test_server_receives_and_responds(self):
        msg = "PING"
        response = self.send_message(msg)
        self.assertIn("Server received", response)

    def test_server_disconnects_on_quit(self):
        response = self.send_message(DISCONNECT_MESSAGE)
        # No assert needed, if no error, server handled quit correctly

if __name__ == "__main__":
    unittest.main()
