import threading
from BotClient import BotClient  # Make sure this import points to your BotClient class

class BotClientManager:
    def __init__(self, num_bots):
        self.num_bots = num_bots
        self.bots = []

    def create_bots(self):
        for _ in range(self.num_bots):
            bot = BotClient()  # Instantiate a BotClient
            self.bots.append(bot)

    def start_bots(self):
        threads = []
        for bot in self.bots:
            thread = threading.Thread(target=bot.run)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def run(self):
        self.create_bots()
        self.start_bots()

# Example usage
if __name__ == "__main__":
    num_bots = 5  # Define the number of bot clients you want to create
    bot_manager = BotClientManager(num_bots)
    bot_manager.run()
