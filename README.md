
## Components

1. **ServerMain**: The core server component responsible for managing trivia games, handling client connections, broadcasting game invitations via UDP, and communicating over TCP for game activities.
2. **ClientMain**: A client program that listens for server broadcasts, connects to the server, and participates in the trivia games by answering questions.
3. **BotClient**: An automated client that simulates player behavior for testing and demonstration purposes. It automatically connects to the server and answers questions based on random choices.
4. **testbot**: Manages multiple instances of `BotClient` for scalable testing.

## Features

- **UDP Broadcast**: Server broadcasts its presence on the network for auto-discovery by clients.
- **TCP Communication**: Secure and reliable communication channel for game sessions between the server and clients.
- **Trivia Management**: Dynamic trivia question handling, scoring, and round management.
- **Concurrency Handling**: Uses threading and `ThreadPoolExecutor` for managing multiple client connections concurrently.
- **Scalable Bot Clients**: Facilitates testing through automated bot clients that can join the game as regular players.


# Trivia Game Network

## Overview
This project implements a trivia game system, consisting of a server that manages the game and clients that participate in trivia sessions. It's designed to demonstrate network programming concepts using UDP for broadcasting and TCP for session management.

## Structure
- **ServerMain.py**: Manages game sessions, handles TCP connections and broadcasts game invitations via UDP.
- **ClientMain.py**: Client that listens for game invitations and connects to the server to participate in the game.
- **BotClient.py**: Automated client designed for testing, which simulates real player actions.
- **TriviaQuestionManager.py**: Manages trivia questions and answers.
- **GameStatistics.py**: Tracks and reports game statistics.
- **Colors.py**: Utility for colored console output to enhance readability.
