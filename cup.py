import random

class Cup:
    def __init__(self):
        """
        Defines an object Cup in a game of Blufpoker.\n
        :param n_dice: Number of dice the cup is initialized with.
        """
        self.dice = []
        for _ in range(3):
            self.dice.append(random.randint(1, 6))

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

    def set_poker(self):
        self.dice = []
        for _ in range(3):
            self.dice.append(3)
        return self.dice

    def roll_dice_with_value(self, value, print_values):
        if value in self.dice:
            # print(f'hand now = {self.dice}')
            self.dice.remove(value)
            new_roll = random.randint(1, 6)
            if print_values: print(f'Rolled die with value {value} to {new_roll}')
            self.dice.append(new_roll)
            self.dice.sort(reverse=True)
            return str(f'rolled die with value {value} to {new_roll}')
        else:
            if print_values: print(f"there is no die of value {value} in the cup")
            return str(f"there is no die of value {value} in the cup")


