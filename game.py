from dice import Die
from player import Player
from cup import Cup
from copy import copy
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
    'start': 0,
    'first_turn': 1,
    'believe/call_bluff_phase': 2,
    'throw_dice_phase': 3,
    'bidding_phase': 4,
    'penalty_phase': 5

}


def random_bid_return():
    i = []
    for _ in range(3):
        i.append(random.randint(1, 6))
    i.sort(reverse=True)

    return i


def print_dice(cup):
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


class Game:
    def __init__(self, n_players=3):
        """
        Main function for initializing the game
        TODO: add state machine, which regulates the turns
        """
        self.players = [Player() for i in range(n_players)]
        self.current_bid = []
        self.n_players = n_players
        self.cup = Cup()
        self.turn = 0
        self.state = states['start']
        self.max_penalty = 3
        self.players[0].throw_strategy = 'lowest'

    def update_turn(self):  # sets turn to the next player
        self.turn = (self.turn + 1) % self.n_players

    def bid_possible(self, bid, strategy):
        if PossibleWorlds.index(self.current_bid) < PossibleWorlds.index(bid):
            print(f'{strategy} bid is possible, {bid} higher than {self.current_bid}')
            # self.print_dice(bid)
            return True
        else:
            print(f'{strategy} bid is impossible, {bid} not higher than {self.current_bid}')
            return False

    def determine_bluff(self, strategy):
        if strategy == 'random':
            if random.randint(1, 100) > 80 or (PossibleWorlds.index(self.current_bid) == len(PossibleWorlds)):  # believe percentage
                return True
            else:
                return False

    def throw_dice(self, throw_strategy):
        dice1 = self.cup.dice[0]
        dice2 = self.cup.dice[1]
        dice3 = self.cup.dice[2]

        if throw_strategy == 'random':
            self.cup.roll_dice_with_value(self.cup.dice[random.randint(0, 2)])

        elif throw_strategy == 'lowest':
            self.cup.roll_dice_with_value(min(self.cup.dice))  # rethrows lowest dice

        elif throw_strategy == 'greedy':
            pass

    def bidding(self, strategy):
        if strategy == 'truthful':
            if self.bid_possible(self.cup.dice, strategy):
                self.current_bid = copy(self.cup.dice)
                # print('[DEBUG] copy the values')
            else:
                random_add = random.randint(1, 3)
                if (PossibleWorlds.index(self.current_bid) + random_add ) < 56:
                    self.current_bid = PossibleWorlds[PossibleWorlds.index(self.current_bid) + random_add ] # bid slightly higher than previous player

                elif (PossibleWorlds.index(self.current_bid) + 1 ) < 56:
                    self.current_bid = PossibleWorlds[PossibleWorlds.index(self.current_bid) + 1 ] # bid slightly higher than previous player

                else: # maximum bid is reached
                    print('WTF do we do now')

    def penalise(self):
        print(f'[PENALISE] The bid was {self.current_bid} and the cup has {self.cup.dice}')
        if PossibleWorlds.index(self.current_bid) > PossibleWorlds.index(self.cup.dice):  # the bid was higher than the cup, previous player was bluffing/lying
            self.players[(self.turn + self.n_players - 1) % self.n_players].penalty_points += 1
            print(f'Player {self.turn} was right, Player {(self.turn + self.n_players - 1) % self.n_players} gets one penalty point') #TODO print Smegma
            self.turn = (self.turn + self.n_players - 1) % self.n_players  # previous player can start again
        else:
            self.players[self.turn].penalty_points += 1
            print(f'Player {self.turn} was wrong and gets one penalty point')
            # turn remains with this player

    def play(self):
        end_game = False
        while not end_game:

            if self.state == states['start']:  # first turn is different than other turns,
                print('------------ NEW ROUND --------------')
                print(f'[STARTING TURN] of Player {self.turn}')
                self.cup.roll_all()
                print(f"[STARTING ROLL] Player {self.turn} throws the dice and rolls:")
                print_dice(self.cup.dice)

                if self.players[self.turn].bid_strategy == 'truthful':
                    self.current_bid = copy(self.cup.dice)
                elif self.players[self.turn].bid_strategy == 'random':
                    self.current_bid = random_bid_return()  # random bid

                print(f"[STARTING BID] Player {self.turn} bids: {self.current_bid}")


                # bid = random_bid_return()
                # if self.bid_possible(bid):
                #     self.current_bid = bid

                input("Press Enter to continue...\n")
                self.update_turn()
                self.state = states['believe/call_bluff_phase']
                continue

            if self.state == states['penalty_phase']:
                self.penalise()

                print('[SCORE] is now as follows:', end=" ")
                for i in range(self.n_players):  # check if a player has lost (i.e has the max penalty points)
                    print(f'Player {i}: {self.players[i].penalty_points} points ', end=" ")
                print()  # print for new line

                for i in range(self.n_players):  # check if a player has lost (i.e has the max penalty points)
                    if self.players[i].penalty_points == self.max_penalty:
                        print(f'Player {i} has {self.max_penalty} penalty points and has lost the game!')
                        end_game = True
                        break

                if not end_game:
                    input("Press Enter to continue...\n")
                self.state = states['start']
                continue


            # ------------- These states are looped within one round --------------

            if self.state == states['believe/call_bluff_phase']:
                print(f'[TURN] of Player {self.turn}')
                if self.determine_bluff(self.players[self.turn].determine_bluff_strategy):  # if true, then agent believes it is a bluff
                    print(f'Player {self.turn} does not believe Player {(self.turn + self.n_players - 1) % self.n_players}')
                    self.state = states['penalty_phase']
                else:
                    print(f'Player {self.turn} believes Player {(self.turn + self.n_players - 1) % self.n_players}')
                    self.state = states['throw_dice_phase']
                input("Press [Enter] to continue...\n")
                continue

            if self.state == states['throw_dice_phase']:
                self.throw_dice(self.players[self.turn].throw_strategy)
                print(f'Player {self.turn} has rolled the dice, the cup is now as follows:')
                print_dice(self.cup.dice)
                input("Press [Enter] to continue...\n")
                self.state = states['bidding_phase']
                continue

            if self.state == states['bidding_phase']:
                self.bidding(self.players[self.turn].bid_strategy)
                print(f'Player {self.turn} has bid: {self.current_bid}')
                input("Press [Enter] to continue...\n")
                self.update_turn()
                self.state = states['believe/call_bluff_phase']
                continue
        print('Game finished!')
