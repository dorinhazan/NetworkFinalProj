import random
import select

from ClientMain import ClientMain

class BotClient(ClientMain):
    def __init__(self, name):
        super().__init__(name)

    def game_mode(self):
        """Enters game mode - automatically answers questions."""
        try:
            while True:
                readable, _, _ = select.select([self.tcp_socket], [], [], None)
                if self.tcp_socket in readable:
                    message = self.tcp_socket.recv(1024).decode().strip()
                    if message:
                        print(f"{self.name} {message}")

                        if "True or false" in message:
                            # Randomly choose an answer
                            answer = random.choice(['Y', 'N'])
                            print(f"{self.name} answer: {answer}")
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
    bot_name = "BOT:" + str(random.randint(1, 100))
    bot = BotClient(bot_name)
    bot.run()
