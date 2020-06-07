import random
from dice import Die


class Player:
    def __init__(self, ):
        """
        Defines an object Player in a game of Blufpoker.\n
        Turn is initialized as false.
        """
        self.knowledge = ['K~p and ~K~Q']
        self.bid = []
        self.turn = False
        self.determine_bluff_strategy = 'random'
        self.throw_strategy = 'random'
        self.bid_strategy = 'truthful'
        self.penalty_points = 0

    def set_bid(self, bidnumbers):
        self.bid = bidnumbers


