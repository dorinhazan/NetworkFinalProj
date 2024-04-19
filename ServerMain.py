import socket
import threading
from threading import Timer
import time
import random
from struct import pack
from concurrent.futures import ThreadPoolExecutor


# Assuming TriviaQuestionManager is implemented elsewhere
from TriviaQuestionManager import TriviaQuestionManager

class ServerMain:
    def __init__(self, port=13117):
        self.udp_broadcast_port = port
        self.clients = {}  # Stores client address and name
        self.trivia_manager = TriviaQuestionManager()
        self.tcp_port = random.randint(1024, 65535)
        base_server_name = "Team Mystic"
        self.server_name = base_server_name.ljust(32)
        self.broadcasting = True  # New attribute to control broadcasting
        self.game_active = False
        self.player_names_server = []
        self.add_number = list(range(1, 501))
        self.executor = ThreadPoolExecutor(max_workers=30)  # Adjust based on expected load
        self.player_names_server_lock = threading.Lock()  # Add a lock for synchronizing access



    def start_udp_broadcast(self):
        """Modified to continuously broadcast using the current TCP port."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as udp_socket:
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            while self.broadcasting:
                # Repack the message with the current TCP port
                message = pack('!Ib32sH', 0xabcddcba, 0x2, self.server_name.encode('utf-8'), self.tcp_port)
                udp_socket.sendto(message, ('<broadcast>', self.udp_broadcast_port))
                time.sleep(2)
    def accept_tcp_connections(self):
        """Accepts TCP connections from clients using a ThreadPoolExecutor."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            bound = False
            attempts = 0
            while not bound and attempts < 50:
                try:
                    tcp_socket.bind(('', self.tcp_port))
                    tcp_socket.listen()
                    print(f"Server started, listening on IP address {socket.gethostbyname(socket.gethostname())}")
                    bound = True
                except socket.error as e:
                    print(f"Port {self.tcp_port} is in use or cannot be bound. Trying another port...")
                    self.tcp_port = random.randint(1024, 65535)
                    attempts += 1

            if not bound:
                print("Failed to bind to a port after several attempts. Exiting.")

                return

            self.wait_for_first_connection(tcp_socket)

    def wait_for_first_connection(self, tcp_socket):
        """Waits for the first connection and starts a timer for accepting more connections."""
        first_client_connected = False

        def stop_accepting_new_connections():
            self.game_active = True
            self.manage_game_rounds()

        while not self.game_active:
            tcp_socket.settimeout(1)  # Short timeout to periodically check if game has started
            try:
                client_socket, addr = tcp_socket.accept()
                self.executor.submit(self.handle_client, client_socket, addr)
                if not first_client_connected:
                    first_client_connected = True
                    Timer(10.0, stop_accepting_new_connections).start()
            except socket.timeout:
                continue

    def handle_client(self, client_socket, addr):
        """Handles communication with a connected client."""
        try:
            player_name = client_socket.recv(1024).decode().strip()
            with self.player_names_server_lock:  # Use the lock when accessing the shared resource
                if not self.check_name_unique(player_name):
                    player_name = player_name + str(self.add_number[0])
                    self.add_number = self.add_number[1:]
                    self.clients[addr] = (player_name, client_socket)
                    self.player_names_server.append(player_name)
                self.clients[addr] = (player_name, client_socket)
                self.player_names_server.append(player_name)


        except Exception as e:
            print(f"Failed to handle client {addr}: {e}")


    def check_name_unique(self, name):
        """Checks if the received name is unique."""
        if name not in self.player_names_server:
            return True
        return False


    def manage_game_rounds(self):
        """Manages the game rounds, ensuring the game continues until there is only one winner."""
        active_players = self.clients.copy()  # Copy the current clients as active players for this round
        # active_players = {addr: client for addr, client in self.clients.items() if client[1]}
        round_number = 1

        while len(active_players) >= 1:
            question, correct_answer = self.trivia_manager.get_random_question()
            question =f'\nTrue or false: {question}\n\n'
            if round_number == 1:
                message = f"Welcome to the Mystic server, where we are answering trivia questions about the Bible.\n"
                for idx, player_name in enumerate(self.clients.values(), start=1):
                    message += f"Player {idx}: {player_name[0]}\n"
                message += "=="+ question
            else:
                players_names = list(active_players.values())
                players_names = [name for name, _ in players_names]
                if len(players_names) > 1:
                    players_list = ', '.join(players_names[:-1]) + ' and ' + players_names[-1]
                else:
                    players_list = players_names[0]
                message = f"\n\nRound {round_number}, played by {players_list}:\n{question}"

            self.broadcast_question(active_players, message)

            # Collect and evaluate answers within a timeout (10 seconds)
            answers = self.collect_answers(active_players)
            winners, active_players = self.evaluate_answers(answers, active_players, correct_answer)

            if len(active_players) == 1 and len(winners) == 0:
                round_number += 1
            elif len(active_players) > 1 and len(winners)>1:
                round_number += 1
            elif len(active_players)==2  and len(winners)==1:
                round_number += 1
            else:
                break  # Exit loop if one player is left

        if active_players:
            self.announce_winner(active_players.keys())  # Announce to all clients
        else:
            no_winners_message = f"\nGame over!\nNo winners"
            for addr, (_, client_socket) in self.clients.items():
                try:
                    client_socket.sendall(no_winners_message.encode('utf-8'))
                except Exception as e:
                    print(f"Failed to announce there are no winners to {self.clients[addr][0]}: {e}")
        self.game_over()

    def broadcast_question(self, active_players, message):
        """Sends the trivia question to all active players."""
        for addr, (player_name, client_socket) in active_players.items():
            try:
                client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting question to player {player_name} at {addr}: {e}")



    def collect_answers(self, active_players):
        """Collects answers from each active player within a specified timeout."""
        answers = {}
        for addr, (player_name, client_socket) in active_players.items():
            try:
                data = client_socket.recv(1024).decode('utf-8').strip().upper()
                if data in ['Y', 'T', '1']:  # Interpreted as True
                    answers[addr] = True
                elif data in ['N', 'F', '0']:  # Interpreted as False
                    answers[addr] = False
                else:
                    answers[addr] = None
            except Exception as e:
                print(f"Failed to receive answer from {player_name}:{e}")

        return answers

    def evaluate_answers(self, answers, active_players, correct_answer):
        """Evaluates the collected answers and updates the list of active players, with specific output formatting."""
        winners = []
        result_messages = {}

        # First, compile the correctness of each answer
        for addr, answer in answers.items():
            if correct_answer == answer:
                winners.append(addr)
                result_messages[addr] = f"{active_players[addr][0]} is correct!"
            elif answer is None:
                result_messages[addr] = f"{active_players[addr][0]} did not respond on time!"
            else:
                result_messages[addr] = f"{active_players[addr][0]} is incorrect!"
                # Instead of deleting here, we will handle incorrect players later

        # Determine the winner(s) and append "Wins!" if there's a single winner
        if len(winners) == 1:
            winner_addr = winners[0]
            winner_name = active_players[winner_addr][0]
            # Add a winning note to the winner's message
            result_messages[winner_addr] += f" {winner_name} Wins!"

        # Compile the broadcast message from individual messages
        broadcast_message = "\n".join(result_messages.values())

        # Remove players who answered incorrectly from active_players for the next round
        for addr in list(
                active_players.keys()):  # Convert to list to avoid 'dictionary changed size during iteration' error
            if addr not in winners:
                del active_players[addr]

        # Broadcast the message to all remaining players
        for addr in self.clients.keys():
            try:
                client_socket = self.clients[addr][1]
                client_socket.sendall(broadcast_message.encode('utf-8'))
            except Exception as e:
                print(f"Failed to send result message: {self.clients[addr][0]} {e}")


        return winners, active_players



    def announce_winner(self, winner_addr):
        winner_addr_tuple = list(winner_addr)[0]
        """Announces the winner to all clients."""
        winner_name, _ = self.clients[winner_addr_tuple]

        winner_message = f"\nGame over!\nCongratulations to the winner: {winner_name}"
        for addr, (_, client_socket) in self.clients.items():
            try:
                client_socket.sendall(winner_message.encode('utf-8'))
            except Exception as e:
                print(f"Failed to announce winner to {self.clients[addr][0]}: {e}")

    def game_over(self):
        """Handles tasks after a game round ends."""
        print("Game over, sending out offer requests...")
        # Close all client connections
        for addr, (_, client_socket) in self.clients.items():
            client_socket.close()
        self.clients.clear()  # Clear the list of clients for the next round
        self.player_names_server.clear()
        self.game_active = False
        self.broadcasting = True  # Enable broadcasting for the next round
        # Optionally, restart the UDP broadcast on a new thread if not automatically restarting
        self.add_number = list(range(1, 501))
        self.start()

    def start(self):
        """Starts the server."""
        threading.Thread(target=self.accept_tcp_connections, daemon=True).start()
        self.start_udp_broadcast()


# Starting the server
if __name__ == "__main__":
    server = ServerMain()
    server.start()