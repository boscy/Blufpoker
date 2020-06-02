import random
from dice import Die


class Cup:
    def __init__(self):
        """
        Defines an object Cup in a game of Blufpoker.\n
        :param n_dice: Number of dice the cup is initialized with.
        """
        self.dice = []
        for _ in range(3):
            self.dice.append(random.randint(1, 6))

        self.dice.sort(reverse = True)

    def roll_all(self):
        """
        Randomly changes the values of the dice in the cup.\n
        :return: The new hand.
        """
        self.dice = []
        for _ in range(3):
            self.dice.append(random.randint(1, 6))
        return self.dice.sort(reverse = True)

    # TODO add rolling one or two die
