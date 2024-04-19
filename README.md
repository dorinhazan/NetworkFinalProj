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

## Features

- **UDP Broadcast**: Server broadcasts its presence on the network for auto-discovery by clients.
- **TCP Communication**: Secure and reliable communication channel for game sessions between the server and clients.
- **Trivia Management**: Dynamic trivia question handling, scoring, and round management.
- **Concurrency Handling**: Uses threading and `ThreadPoolExecutor` for managing multiple client connections concurrently.
- **Scalable Bot Clients**: Facilitates testing through automated bot clients that can join the game as regular players.
