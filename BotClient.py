import random
import select
import time
from ClientMain import ClientMain
from Colors import Colors



class BotClient(ClientMain):
    """
    BotClient extends ClientMain to interact with a game server automatically.
    """
    def __init__(self):
        """Initialize the bot client by calling the superclass's initializer."""
        super().__init__()

    # Overriding the game_mode method
    def game_mode(self):
        """
          Handles the game mode by listening for server messages and responding to game prompts.

          Continuously listens for messages from the server over a TCP socket. On receiving a 'True or false' prompt,
          it automatically sends a random answer after a short delay. If a 'Game over!' message is received, it breaks
          the loop and ends the game session.
        """
        try:
            game_over_received = False
            while not game_over_received:
                # Block until there are sockets ready for reading

                readable, _, _ = select.select([self.tcp_socket], [], [], None)
                if self.tcp_socket in readable:
                    # self.send_heartbeat()
                    try:
                        message = self.tcp_socket.recv(1024).decode().strip()
                        if message != '':
                            print(f"\n{message}") # Print the message from the server
                            if "Game over!" in message:
                                game_over_received = True # End the loop if game over message is received
                                break
                            if "True or false" in message:
                                # Start a timer for 10 seconds to wait for an answer
                                start_time = time.time()
                                while (time.time() - start_time) < 10:
                                    # Simulate a delay in response to make bot's behavior more realistic
                                    time.sleep(5)
                                    answer = random.choice(['Y', '1', 'T', 'N', '0', 'F'])
                                    # self.send_heartbeat()
                                    self.tcp_socket.sendall(answer.encode())
                                    break
                        else:
                            # if message from server is empty - close connection
                            self.tcp_socket.close()
                            self.listen_for_udp_broadcast()

                    except Exception as e:
                        print(f"{Colors.RED}KeyBoardInterapt {Colors.END}")

        except Exception as e:
            print(f"{Colors.RED}[Bot {self.name}] An error occurred: {e}{Colors.END}")

        finally:
            # Close the connection and prepare for a possible new game or connection
            print(f"{Colors.END}Server disconnected, listening for offer requests...\n")
            self.tcp_socket.close()
            self.listen_for_udp_broadcast()

    def run(self):
        """
        Main loop to continuously try connecting and playing the game.

        It sets a random name for the bot, listens for server broadcasts, connects to the game server,
        and enters the game mode. If an error occurs, it attempts to reconnect after closing any existing socket.
        """
        while True:
            try:
                self.name = "Bot:" + random.choice(self.player_names)
                self.listen_for_udp_broadcast()
                self.connect_to_server()
                self.game_mode()

            except Exception as e:
                print(f"{Colors.RED}Error encountered: {e}. Attempting to reconnect...{Colors.END}")

                if self.tcp_socket:
                    self.tcp_socket.close()  # Ensure the socket is closed before retrying



if __name__ == "__main__":
    bot = BotClient()
    bot.run()
