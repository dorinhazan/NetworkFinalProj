import random
import select
import time
from ClientMain import ClientMain
from Colors import Colors



class BotClient(ClientMain):
    def __init__(self):
        super().__init__()

    # Overriding the game_mode method
    def game_mode(self):
        """Enters game mode - automatically answers questions."""
        try:
            game_over_received = False
            while not game_over_received:
                readable, _, _ = select.select([self.tcp_socket], [], [], None)
                if self.tcp_socket in readable:
                    message = self.tcp_socket.recv(1024).decode().strip()
                    if message:
                        print(f"\n{message}\n")
                        if "Game over!" in message:
                            game_over_received = True
                            break
                        if "True or false" in message:
                            # Start a timer for 10 seconds to wait for an answer

                            start_time = time.time()
                            while (time.time() - start_time) < 10:
                                time.sleep(4)
                                answer = random.choice(['Y', '1', 'T', 'N', '0', 'F'])
                                self.tcp_socket.sendall(answer.encode())
                                break
        except Exception as e:
            print(f"{Colors.RED}[Bot {self.name}] An error occurred: {e}")
        finally:

            print(f"{Colors.END}Server disconnected, listening for offer requests...")

            self.tcp_socket.close()
            self.listen_for_udp_broadcast()

    def run(self):
        while True:
            time.sleep(1)

            try:
                self.name = "Bot:" + random.choice(self.player_names)
                self.listen_for_udp_broadcast()
                self.connect_to_server()
                self.game_mode()
            except Exception as e:
                print(f"{Colors.RED}Error encountered: {e}. Attempting to reconnect...")

                if self.tcp_socket:
                    self.tcp_socket.close()  # Ensure the socket is closed before retrying


if __name__ == "__main__":
    bot = BotClient()
    bot.run()

