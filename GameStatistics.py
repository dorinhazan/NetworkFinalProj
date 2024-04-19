class GameStatistics:
    def _init_(self):
        self.best_team_ever = None
        self.best_score_ever = 0
        self.character_frequency = {}
        self.total_games_played = 0
        self.total_answers_received = 0

    def update_statistics(self, game_data):
        """
        Update statistics based on the results of a single game.
        :param game_data: dict with keys 'team_scores' and 'answers'
        """
        self.total_games_played += 1
        self.update_best_team_ever(game_data['team_scores'])
        self.update_character_frequency(game_data['answers'])

    def update_best_team_ever(self, team_scores):
        """
        Determines if the current game has the best team score ever and updates.
        :param team_scores: dict of team names and their scores
        """
        for team, score in team_scores.items():
            if score > self.best_score_ever:
                self.best_score_ever = score
                self.best_team_ever = team

    def update_character_frequency(self, answers):
        """
        Updates the frequency of each character typed by players.
        :param answers: list of strings (answers) from players
        """
        for answer in answers:
            for char in answer:
                if char in self.character_frequency:
                    self.character_frequency[char] += 1
                else:
                    self.character_frequency[char] = 1
        self.total_answers_received += len(answers)

    def get_most_common_character(self):
        """
        Returns the most commonly typed character.
        """
        if not self.character_frequency:
            return None
        return max(self.character_frequency, key=self.character_frequency.get)

    def display_statistics(self):
        """
        Prints the collected statistics.
        """
        print(f"Total games played: {self.total_games_played}")
        print(f"Best team ever: {self.best_team_ever} with a score of {self.best_score_ever}")
        most_common_char = self.get_most_common_character()
        print(f"Most commonly typed character: {most_common_char} (used {self.character_frequency.get(most_common_char, 0)} times)")
        print(f"Total answers received: {self.total_answers_received}")

# Example usage within the server
if __name__ == "_main_":
    stats = GameStatistics()
    example_game_data = {
        'team_scores': {'Team Mystic': 100, 'Team Valor': 95},
        'answers': ['yes', 'no', 'yes', 'True', 'False']
    }
    stats.update_statistics(example_game_data)
    stats.display_statistics()
