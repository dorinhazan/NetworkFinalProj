import socket
import threading
import time
import random
from struct import pack

# Assuming TriviaQuestionManager is implemented elsewhere
from TriviaQuestionManager import TriviaQuestionManager


class ServerMain:
    def __init__(self, port=13117):
        self.port = port
        self.clients = {}  # Stores client address and name
        self.trivia_manager = TriviaQuestionManager()
        self.udp_broadcast_port = 13117
        self.tcp_port = random.randint(1024, 65535)
        base_server_name = "Team Mystic"
        self.server_name = base_server_name.ljust(32)

        self.game_active = False

    def start_udp_broadcast(self):
        """Broadcasts server presence via UDP."""
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        print(f"Team Mystic starts their server. The server prints out “Server started, listening on IP address {socket.gethostbyname(socket.gethostname())}")
        message = pack('!Ib32sh', 0xabcddcba, 0x2, self.server_name.encode('utf-8'), self.tcp_port)

        while not self.game_active:
            udp_socket.sendto(message, ('<broadcast>', self.udp_broadcast_port))
            time.sleep(1)
        udp_socket.close()

    def accept_tcp_connections(self):
        """Accepts TCP connections from clients, handling port in use."""
        bound = False
        attempts = 0

        while not bound and attempts < 5:
            try:
                tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_socket.bind(('', self.tcp_port))
                tcp_socket.listen()
                print(
                    f"Server started, listening on IP address {socket.gethostbyname(socket.gethostname())} on port {self.tcp_port}")
                bound = True
            except socket.error as e:
                print(f"Port {self.tcp_port} is in use or cannot be bound. Trying another port...")
                attempts += 1
                tcp_socket.close()  # Ensure the socket is closed before retrying

        if not bound:
            print("Failed to bind to a port after several attempts. Exiting.")
            return

        start_time = time.time()

        while time.time() - start_time < 10:  # Accept connections for 10 seconds
            tcp_socket.settimeout(10 - (time.time() - start_time))
            try:
                conn, addr = tcp_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.start()
            except socket.timeout:
                break

        self.game_active = True
        self.manage_game_rounds()

    def handle_client(self, conn, addr):
        """Handles communication with a connected client."""
        player_name = conn.recv(1024).decode().strip()
        self.clients[addr] = player_name

    def manage_game_rounds(self):
        """Manages the game rounds, ensuring the game continues until there is only one winner."""
        active_players = self.clients.copy()  # Copy the current clients as active players for this round

        round_number = 1

        while len(active_players) > 1:
            question, correct_answer = self.trivia_manager.get_random_question()

            if round_number == 1:
                message = f"Welcome to the Mystic server, where we are answering trivia questions about Aston Villa FC.\n"
                for idx, player_name in enumerate(self.clients.values(), start=1):
                    message += f"Player {idx}: {player_name}\n"
                message += "=="+ "\nTrue or false: " + question
            else:
                players_names = list(active_players.values())
                if len(players_names) > 1:
                    players_list = ', '.join(players_names[:-1]) + ' and ' + players_names[-1]
                else:
                    players_list = players_names[0]
                message = f"Round {round_number}, played by {players_list}:\nTrue or false: {question}"

            self.broadcast_question(active_players, question)

            # Collect and evaluate answers within a timeout (10 seconds)
            answers = self.collect_answers(active_players)
            winners, active_players = self.evaluate_answers(answers, active_players, correct_answer)

            # Prepare for next round if necessary
            if len(active_players) > 1:
                print(f"Moving to Round {round_number + 1}")
                round_number += 1
            else:
                break  # Exit loop if one player is left

        # Announce game winner
        if active_players:
            self.announce_winner(active_players.keys()[0])  # Announce to all clients
        else:
            print("No winners.")

    def broadcast_question(self, active_players, message):
        """Sends the trivia question to all active players."""
        for conn in active_players.keys():
            try:
                conn.sendall(message.encode('utf-8'))
            except Exception as e:
                player_name = active_players[conn]
                print(f"Error broadcasting question to player {player_name}: {e}")

    def collect_answers(self, active_players):
        """Collects answers from each active player within a specified timeout."""
        answers = {}
        for conn in list(active_players.keys()):
            conn.settimeout(10)  # 10 seconds to answer
            try:
                data = conn.recv(1024).strip().upper()
                if data in ["Y,T,1","N,F,0"]:  # Acceptable answers
                    answers[conn] = data
            except socket.timeout:
                print(f"{active_players[conn]} did not respond in time.")
            except Exception as e:
                print(f"Error collecting answer from {active_players[conn]}: {e}")
        return answers

    def evaluate_answers(self, answers, active_players, correct_answer):
        """Evaluates the collected answers and updates the list of active players, with specific output formatting."""
        winners = []
        # Temporarily store messages to decide if we append "Wins!" for a single winner
        result_messages = []

        # Evaluate each answer and prepare their result message
        for conn, answer in answers.items():
            if correct_answer == answer:
                winners.append(conn)
                result_messages.append(f"{active_players[conn]} is correct!")
            else:
                result_messages.append(f"{active_players[conn]} is incorrect!")
                del active_players[conn]  # Remove player if they answered incorrectly

        # Determine if a single winner message needs to be adjusted
        if len(winners) == 1:
            # If there's only one winner, append "Wins!" to their message
            winner_name = active_players[winners[0]]
            for i, msg in enumerate(result_messages):
                if winner_name in msg:
                    result_messages[i] = msg + " " + winner_name + " Wins!"

        # Print all result messages
        for msg in result_messages:
            print(msg)

        return winners, active_players

    def announce_winner(self, winner_conn):
        """Announces the winner to all clients."""
        winner_message = f"Game over! Congratulations to the winner: {self.clients[winner_conn]}"
        for conn in self.clients.keys():
            try:
                conn.sendall(winner_message.encode('utf-8'))
            except Exception as e:
                print(f"Failed to announce winner to {self.clients[conn]}: {e}")

    def start(self):
        """Starts the server."""
        threading.Thread(target=self.start_udp_broadcast).start()
        self.accept_tcp_connections()


# Starting the server
if __name__ == "__main__":
    server = ServerMain()
    server.start()
