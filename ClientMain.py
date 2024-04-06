import socket
import select
import struct


class ClientMain:
    def __init__(self, name):
        self.name = name
        self.server_ip = None
        self.server_port = None
        self.tcp_socket = None

    def listen_for_udp_broadcast(self):
        """Listens for UDP broadcast to discover the server."""
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.bind(('', 13117))  # Assuming 13117 is the broadcast port

        print("Client started, listening for offer requests...")
        while True:
            data, addr = udp_socket.recvfrom(1024)

            magic_cookie, message_type = struct.unpack('!Ib', data[:5])
            # Directly extract the server port from the correct position
            server_port = struct.unpack('!H', data[-2:])[0]  # Extract the last 2 bytes for the server port

            if magic_cookie == 0xabcddcba and message_type == 0x2:
                self.server_ip = addr[0]
                self.server_port = server_port

                print(f"Received offer from server at address {self.server_ip}, attempting to connect... {self.server_port}")
                udp_socket.close()
                break

    def connect_to_server(self):
        """Connects to the server over TCP and sends the player name."""
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect((self.server_ip, self.server_port))
        self.tcp_socket.sendall((self.name + '\n').encode())



    def game_mode(self):
        """Enters game mode - sending answers and receiving questions."""
        try:
            while True:
                readable, _, _ = select.select([self.tcp_socket], [], [], None)
                if self.tcp_socket in readable:
                    message = self.tcp_socket.recv(1024).decode().strip()
                    if message:
                        print(f"Received message: {message}")

                        if "True or false" in message:
                            answer = input("Your answer (Y/N): ").strip().upper()
                            self.tcp_socket.sendall(answer.encode())
                    else:
                        break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Server disconnected, listening for offer requests...")
            self.tcp_socket.close()

    def run(self):
        """Runs the client."""
        self.listen_for_udp_broadcast()
        self.connect_to_server()
        self.game_mode()

# Example usage
if __name__ == "__main__":
    client_name = input("Enter your name: ")
    client = ClientMain(client_name)
    client.run()
