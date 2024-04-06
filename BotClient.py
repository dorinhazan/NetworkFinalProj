import random
from ClientMain import ClientMain  # Assuming ClientMain is in the same directory or correctly imported

class BotClient(ClientMain):
    def __init__(self, name):
        # Call the superclass constructor to initialize inherited properties
        super().__init__(name)

    def game_mode(self):
        """Enters game mode - automatically answers questions."""
        try:
            while True:
                readable, _, _ = select.select([self.tcp_socket], [], [], None)
                if self.tcp_socket in readable:
                    message = self.tcp_socket.recv(1024).decode().strip()
                    if message:
                        print(f"[Bot {self.name}] Received message: {message}")

                        if "True or false" in message:
                            # Randomly choose an answer
                            answer = random.choice(['Y', 'N'])
                            print(f"[Bot {self.name}] Auto-answering: {answer}")
                            self.tcp_socket.sendall(answer.encode())
                    else:
                        break
        except Exception as e:
            print(f"[Bot {self.name}] An error occurred: {e}")
        finally:
            print(f"[Bot {self.name}] Server disconnected, listening for offer requests...")
            self.tcp_socket.close()

# Example usage
if __name__ == "__main__":
    bot_name = "Bot_" + str(random.randint(1, 100))  # Randomly generate a bot name
    bot = BotClient(bot_name)
    bot.run()
