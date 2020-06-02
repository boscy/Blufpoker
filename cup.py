import random
from dice import Die


class Cup:
    def __init__(self):
        """
        Defines an object Cup in a game of Blufpoker.\n
        :param n_dice: Number of dice the cup is initialized with.
        """
        self.dice = [3,1,1]
        # for _ in range(3):
        #     self.dice.append(random.randint(1, 6))

        self.dice.sort(reverse=True)

    def roll_all(self):
        """
        Randomly changes the values of the dice in the cup.\n
        :return: The new hand.
        """
        self.dice = []
        for _ in range(3):
            self.dice.append(random.randint(1, 6))
        return self.dice.sort(reverse=True)

    def roll_dice_with_value(self, value):
        if value in self.dice:
            print(f'hand now = {self.dice}')
            print(f'removing dice with value {self.dice.index(value)}')
            self.dice.remove(value)
            self.dice.append(random.randint(1, 6))
            self.dice.sort(reverse=True)
        else:
            print(f"there is no dice of value {value} in the cup")

    # TODO add rolling one or two die, add which dice are visible and not
