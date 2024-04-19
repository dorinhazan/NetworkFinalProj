from ClientMain import ClientMain
import threading
import random

class AutomatedClient(ClientMain):
    def __init__(self, name):
        super().__init__(name)
        # Automatically set the client's name during initialization

    def run(self):
        """Overrides the run method to automatically connect to the server and enter the game mode."""
        self.connect_to_server()
        self.game_mode()

    def connect_to_server(self):
        """Connect to the server automatically, omitting the input step."""
        # Assuming connect_to_server() in ClientMain connects to the server
        super().connect_to_server()
        print(f"{self.name} connected to the server.")

    def game_mode(self):
        """Simulate game interaction by automatically sending answers."""
        # In ClientMain, replace or complement the logic for waiting for a question and sending a response
        # For simulation, we'll just print an automatic response
        automatic_answer = random.choice(['Y', 'N'])  # Randomly chooses 'Y' or 'N'
        print(f"{self.name} automatically answering: {automatic_answer}")
        # Here, you should actually send the answer to the server if in a real scenario

def create_and_run_client(client_id):
    client_name = f"Player_{client_id}"
    client = AutomatedClient(client_name)
    client.run()

if __name__ == "__main__":
    number_of_clients = 5  # For example, creating 5 clients
    threads = []

    for i in range(number_of_clients):
        thread = threading.Thread(target=create_and_run_client, args=(i+1,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()