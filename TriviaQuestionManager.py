import random

class TriviaQuestionManager:
    """
    Manages a collection of trivia questions related to biblical events and figures.
    This class provides functionality to randomly select trivia questions from a predefined list.
    """
    def __init__(self):
        self.questions = [
            {"text": "Moses was the first king of Israel.", "is_true": False},
            {"text": "David defeated Goliath with a sling and a stone.", "is_true": True},
            {"text": "Jonah was swallowed by a big fish for three days and three nights.", "is_true": True},
            {"text": "The Sermon on the Mount was delivered on Mount Sinai.", "is_true": False},
            {"text": "Paul's original name was Saul.", "is_true": True},
            {"text": "The book of Revelation is the last book of the New Testament.", "is_true": True},
            {"text": "Jesus was baptized by Peter.", "is_true": False},
            {"text": "The Exodus is the story of the Israelites' escape from Egypt.", "is_true": True},
            {"text": "The fruit Eve ate from the forbidden tree was an apple.", "is_true": False},  # The type of fruit is not specified.
            {"text": "Solomon asked God for wisdom to rule Israel wisely.", "is_true": True},
            {"text": "Jesus turned water into wine as his first recorded miracle.", "is_true": True},
            {"text": "The Ten Commandments were given to Moses on Mount Ararat.", "is_true": False},  # They were given on Mount Sinai.
            {"text": "Peter denied Jesus three times before the rooster crowed.", "is_true": True},
            {"text": "Judas Iscariot was the disciple who betrayed Jesus for thirty pieces of silver.", "is_true": True},
            {"text": "Noah's Ark rested on Mount Everest after the flood.", "is_true": False},  # It rested on Mount Ararat.
            {"text": "The walls of Jericho fell after the Israelites marched around them for seven days.", "is_true": True},
            {"text": "There are four Gospels in the New Testament: Matthew, Mark, Luke, and John.", "is_true": True},
            {"text": "Ruth was the first female judge of Israel.", "is_true": False},  # Deborah was a judge; Ruth was not a judge.
            {"text": "Lazarus was raised from the dead by Jesus.", "is_true": True},
            {"text": "The Apostle Paul wrote most of the New Testament.", "is_true": True},
        ]

    def get_random_question(self):
        """Returns a random trivia question and its answer."""
        # Randomly choose one question from the list of questions.
        question = random.choice(self.questions)
        return question["text"], question["is_true"]

