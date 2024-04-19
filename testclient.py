import asyncio
import random
from ClientMain import ClientMain
from BotClient import BotClient
import threading
import time

class ClientManager:
    def __init__(self, num_clients):
        self.num_clients = num_clients
        self.clients = []

    def create_clients(self):
        for _ in range(self.num_clients):
            client = ClientMain()
            self.clients.append(client)

    def start_clients(self):
        threads = []
        for client in self.clients:
            thread = threading.Thread(target=client.run)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def run(self):
        self.create_clients()
        self.start_clients()

# Example usage
if __name__ == "__main__":
    num_clients = 5  # Define the number of clients you want to create
    client_manager = ClientManager(num_clients)
    client_manager.run()