# Trivia Game Server and Client System

## Overview

This repository contains the code for a multiplayer trivia game system that operates over a network. The system consists of a server that hosts the trivia game and multiple clients (including bot clients) that connect to the server to participate in the game.

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
