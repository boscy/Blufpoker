from dice import Die
from player import Player
from cup import Cup
import random

PossibleWorlds = [
    [2, 1, 1], [2, 2, 1],
    [3, 1, 1], [3, 2, 1], [3, 2, 2], [3, 3, 1], [3, 3, 2],
    [4, 1, 1], [4, 2, 1], [4, 2, 2], [4, 3, 1], [4, 3, 2], [4, 3, 3], [4, 4, 1], [4, 4, 2], [4, 4, 3],
    [5, 1, 1], [5, 2, 1], [5, 2, 2], [5, 3, 1], [5, 3, 2], [5, 3, 3], [5, 4, 1], [5, 4, 2], [5, 4, 3], [5, 4, 4],
    [5, 5, 1], [5, 5, 2], [5, 5, 3], [5, 5, 4],
    [6, 1, 1], [6, 2, 1], [6, 2, 2], [6, 3, 1], [6, 3, 2], [6, 3, 3], [6, 4, 1], [6, 4, 2], [6, 4, 3], [6, 4, 4],
    [6, 5, 1], [6, 5, 2], [6, 5, 3], [6, 5, 4], [6, 5, 5], [6, 6, 1], [6, 6, 2], [6, 6, 3], [6, 6, 4], [6, 6, 5],
    [1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5], [6, 6, 6]
]

states = {  # states that a player runs through
    'end': 0,
    'start': 1,
    'first_turn': 2,
    'believe/call_bluff_phase': 3,
    'throw_dice_phase': 4,
    'bidding_phase': 5
}


def random_bid_return():
    i = []
    for _ in range(3):
        i.append(random.randint(1, 6))
    i.sort(reverse=True)

    return i


class Game:
    def __init__(self, n_players=3):
        """
        Main function for initializing the game
        TODO: add state machine, which regulates the turns
        """
        self.players = [Player() for i in range(n_players)]
        # self.p1 = Player()
        # self.p2 = Player()
        # self.p3 = Player()
        self.current_bid = []
        self.cup = Cup()
        self.players[0].turn = True
        self.state = states['start']

    def print_dice(self, cup):
        base = '+---------+         +---------+         +---------+'
        sep = '         '
        blank = '|         |'
        left = '| o       |'
        middle = '|    o    |'
        right = '|       o |'
        both = '| o     o |'

        dice = [(blank, middle, blank),
                (left, blank, right),
                (left, middle, right),
                (both, blank, both),
                (both, middle, both),
                (both, both, both)]
        print(base)
        print('\n'.join(a + sep + b + sep + c for a, b, c in zip(dice[cup[0] - 1], dice[cup[1] - 1], dice[cup[2] - 1])))
        print(base)

    def update_turn(self): #sets turn to the next player
        #TODO make this function more generic
        if self.players[0].turn:
            self.players[1].turn = True
            self.players[0].turn = False
        elif self.players[1].turn:
            self.players[2].turn = True
            self.players[1].turn = False
        elif self.players[2].turn:
            self.players[0].turn = True
            self.players[2].turn = False

    def bid_possible(self, bid):
        if PossibleWorlds.index(self.current_bid) < PossibleWorlds.index(bid):
            print(f'bid possible, {bid} higher than {self.current_bid}')
            self.print_dice(bid)
            return True
        else:
            print(f'bid impossible, {bid} not higher than {self.current_bid}')
            return False

    def play(self):
        if self.state == states['start']:  # first turn is different than other turns
            self.cup.roll_all()
            print("cup roll:")
            self.print_dice(self.cup.dice)

            bid = random_bid_return()
            self.current_bid = bid

            print("bid:")
            self.print_dice(self.current_bid)

            bid = random_bid_return()
            if self.bid_possible(bid):
                self.current_bid = bid







