from player import Player
from cup import Cup
from copy import copy, deepcopy
import random
import numpy as np
from visualize_dice import Visualized_game

losscount = [0, 0, 0]

AllPossibleWorlds = [  # ordered from low to high
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
    'roll_dice_phase': 3,
    'bidding_phase': 4,
    'penalty_phase': 5,
    'poker_phase': 6
}


def is_poker(bid):
    if bid[0] == bid[1] and bid[1] == bid[2]:
        return True
    else:
        return False


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


def make_jpd(options, pk):  # makes a joint probability of the possible rolls, for calculating chances

    jpd = [deepcopy(options), [0] * len(options)]
    for i in range(len(jpd[0])):
        if len(pk) == 0:  # three unknown dice
            if jpd[0][i][0] == jpd[0][i][1] == jpd[0][i][2]:  # three equal dice
                jpd[1][i] = 1 / 216  # chance equal to (1/6)^3
            elif jpd[0][i][0] == jpd[0][i][1] or jpd[0][i][0] == jpd[0][i][2] or jpd[0][i][1] == jpd[0][i][
                2]:  # two dice are the same
                jpd[1][i] = 3 / 216
            else:  # all dice are different
                jpd[1][i] = 6 / 216

        elif len(pk) == 1:  # two unknown dice
            working_prob = deepcopy(jpd[0][i])
            working_prob.remove(pk[0])
            if working_prob[0] == working_prob[1]:  # chance to roll the same dice
                jpd[1][i] = 1 / 36
            else:
                jpd[1][i] = 2 / 36

        elif len(pk) == 2:  # one unknown dice > probability is 1/6 for all dice rolls
            jpd[1][i] = 1 / 6

    return jpd


class Game:
    def __init__(self, n_players=3, print_info=True, press_to_continue=False, visualise_game_gui=True, mean_th=3 / 12):
        """
        Main function for initializing the game
        """
        self.players = [Player() for _ in range(n_players)]
        self.end_game = False
        self.first_turn = True
        self.current_bid = []
        self.public_knowledge = []
        self.not_public_knowledge = []
        self.n_players = n_players
        self.cup = Cup()
        self.turn = random.randint(0, n_players - 1)  # first turn is random
        self.state = states['start']
        self.loser_name = ['H', 'O', 'R', 'S', 'E']  # TODO make is such that user can set this.
        self.max_penalty = len(self.loser_name)
        self.max_overbid = 3
        self.believe_threshold_mean = mean_th
        self.gui_print = ''

        self.print_info = print_info  #
        self.press_to_continue = press_to_continue
        self.visualise_game_gui = visualise_game_gui

        ############# Agent strategies configuration ######################

        self.players[0].roll_strategy = 'random'
        self.players[0].bid_strategy = 'truthful'
        self.players[0].determine_bluff_strategy = 'random'

        # self.players[0].roll_strategy = 'random_lowest'
        # self.players[0].bid_strategy = 'truthful'
        # self.players[0].determine_bluff_strategy = 'always_true'

        # self.players[1].roll_strategy = 'random'
        # self.players[1].bid_strategy = 'truthful'
        # self.players[1].determine_bluff_strategy = 'random'

        self.players[1].roll_strategy = '1_lowest'
        self.players[1].bid_strategy = 'always_overbid'
        self.players[1].determine_bluff_strategy = 'always_true'

        self.players[2].roll_strategy = 'knowledge_based'
        self.players[2].bid_strategy = 'knowledge_based'
        self.players[2].determine_bluff_strategy = 'knowledge_based'

        # self.players[1].roll_strategy = 'knowledge_based'
        # self.players[1].bid_strategy = 'knowledge_based'
        # self.players[1].determine_bluff_strategy = 'knowledge_based'
        #
        # self.players[0].roll_strategy = 'knowledge_based'
        # self.players[0].bid_strategy = 'knowledge_based'
        # self.players[0].determine_bluff_strategy = 'knowledge_based'

    def update_turn(self):  # sets turn to the next player
        self.turn = (self.turn + 1) % self.n_players

    def bid_possible(self, bid):
        if AllPossibleWorlds.index(self.current_bid) < AllPossibleWorlds.index(bid):
            if self.print_info: print(f'Truthful bid is possible, {bid} higher than {self.current_bid}')
            # self.if self.print_info: print_dice(bid)
            return True
        else:
            if self.print_info: print(f'Truthful bid is impossible, {bid} not higher than {self.current_bid}')
            return False

    def determine_bluff(self, strategy):
        if strategy == 'random':
            believe_percentage = 80
            if random.randint(1, 100) > believe_percentage or (  # believing probability
                    AllPossibleWorlds.index(self.current_bid) == len(AllPossibleWorlds) - 1):

                return True

            else:

                return False

        elif strategy == 'always_true':  # believes > no bluff

            return False

        elif strategy == 'always_false':

            return True

        elif strategy == 'knowledge_based':
            if self.current_bid not in self.players[self.turn].knowledge:
            #TODO, fix for low bids that knowledge agent does always call bluff
                return True

            else:

                jpd = make_jpd(self.players[self.turn].knowledge,
                               self.public_knowledge)  # make a joint probability distribution of the possible rolls
                # if self.print_info: print(jpd)
                higher_possible = [w for w in self.players[self.turn].knowledge if
                                   self.players[self.turn].knowledge.index(w) >= self.players[
                                       self.turn].knowledge.index(self.current_bid)]

                lower_possible = [w for w in self.players[self.turn].knowledge if
                                  self.players[self.turn].knowledge.index(w) < self.players[
                                      self.turn].knowledge.index(self.current_bid)]

                probability = 0
                for w in higher_possible:
                    # if self.print_info: print(w)
                    if w in jpd[0]:
                        probability += jpd[1][jpd[0].index(w)]

                if self.print_info: print(
                    f'Probability of rolling possible higher worlds among possible worlds: {probability}')

                # add variable threshold depending on public knowledge (since belief probability depends on proportion of possible worlds, which is more variable with less pk)

                if len(self.public_knowledge) == 2:
                    believe_threshold = np.random.normal(self.believe_threshold_mean, 1 / 12, 1)
                elif len(self.public_knowledge) == 1:
                    believe_threshold = np.random.normal(self.believe_threshold_mean, 1 / 12, 1) * 0.75
                else:
                    believe_threshold = np.random.normal(self.believe_threshold_mean, 1 / 12, 1) * 0.5

                # NOTE this believe threshold will always have some kind of arbitrariness, which is due to uncertainty. But this is also the case for human players
                # Finding the correct normal distribution is quite hard.

                if probability >= believe_threshold:
                    if self.print_info: print(f' {probability} >= {believe_threshold}')

                    return False  # not a bluff -> believe
                else:
                    if self.print_info: print(f' {probability} < {believe_threshold}')

                    return True

    def roll_dice(self, roll_strategy):
        # dice are always ordered, so ranked from highest to lowest
        # maintain which dice are rolled, such that we can know what can be set as public knowledge
        dicecopy = [deepcopy(self.cup.dice), [0, 0, 0]]  # make a copy of the dice and whether they are rolled

        # roll according to strategies 'random', '1_lowest', 'random_lowest', 'greedy', 'knowledge_based'
        if roll_strategy == 'random':
            if self.print_info: print('[ROLL] Rolling random die')
            randomDie = random.randint(0, 2)
            self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][randomDie], self.print_info)
            dicecopy[1][randomDie] = 1
            if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                        know1=self.players[0].knowledge,
                                                        know2=self.players[1].knowledge,
                                                        know3=self.players[2].knowledge, turn=self.turn,
                                                        penal1=self.players[0].penalty_points,
                                                        penal2=self.players[1].penalty_points,
                                                        penal3=self.players[2].penalty_points,
                                                        losername=self.loser_name,
                                                        current_bid=self.current_bid, text='', printtext=self.gui_print)

        elif roll_strategy == '1_lowest':
            if self.print_info: print('[ROLL] Rolling 1 lowest die ')
            self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][2], self.print_info)  # rolls the lowest die
            dicecopy[1][2] = 1
            if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                        know1=self.players[0].knowledge,
                                                        know2=self.players[1].knowledge,
                                                        know3=self.players[2].knowledge, turn=self.turn,
                                                        penal1=self.players[0].penalty_points,
                                                        penal2=self.players[1].penalty_points,
                                                        penal3=self.players[2].penalty_points,
                                                        losername=self.loser_name,
                                                        current_bid=self.current_bid, text='', printtext=self.gui_print)

        elif roll_strategy == 'random_lowest':
            if self.print_info: print(
                '[ROLL] Rolling random n lowest dice')  # rolls the n lowest dice, with n randomly determined
            random_n = random.randint(0, 2)
            self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][2], self.print_info)
            dicecopy[1][2] = 1
            if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                        know1=self.players[0].knowledge,
                                                        know2=self.players[1].knowledge,
                                                        know3=self.players[2].knowledge, turn=self.turn,
                                                        penal1=self.players[0].penalty_points,
                                                        penal2=self.players[1].penalty_points,
                                                        penal3=self.players[2].penalty_points,
                                                        losername=self.loser_name,
                                                        current_bid=self.current_bid, text='', printtext=self.gui_print)
            if random_n > 0:  # must be done dice by dice since reshuffle disallows a loop
                self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][1], self.print_info)
                dicecopy[1][1] = 1
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)
            if random_n > 1:
                self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][0], self.print_info)
                dicecopy[1][0] = 1
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)

        elif roll_strategy == 'greedy':  # rolls all dice that aren't 6's
            if self.print_info: print('[ROLL] Rolling greedy (all non-6 dice)')
            if dicecopy[0][0] != 6:
                self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][0], self.print_info)
                dicecopy[1][0] = 1
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)
            if dicecopy[0][1] != 6:
                self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][1], self.print_info)
                dicecopy[1][1] = 1
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)
            if dicecopy[0][2] != 6:
                self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][2], self.print_info)
                dicecopy[1][2] = 1
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)

        elif roll_strategy == 'knowledge_based':
            # Knowledge based rolling strategy

            self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][
                                                                2],
                                                            self.print_info)  # always rolls the lowest die first, this always has the highest chance of getting to a higher bet
            dicecopy[1][2] = 1
            if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                        know1=self.players[0].knowledge,
                                                        know2=self.players[1].knowledge,
                                                        know3=self.players[2].knowledge, turn=self.turn,
                                                        penal1=self.players[0].penalty_points,
                                                        penal2=self.players[1].penalty_points,
                                                        penal3=self.players[2].penalty_points,
                                                        losername=self.loser_name,
                                                        current_bid=self.current_bid, text='', printtext=self.gui_print)
            if not self.bid_possible(
                    self.cup.dice):  # if the cup is not higher than the bid, make decision whether to roll another die or bluff
                if self.print_info: print('First roll did not cause for a higher value than the current bid')
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                # implement small chance (1/6) of bluffing on poker in bidding round, if two dice can be displayed
                if dicecopy[0][0] == dicecopy[0][1] and random.randint(0, 1000) < 167:  # first two dice are the same
                    self.players[self.turn].bluff_poker = True
                    self.players[self.turn].bluff_value = dicecopy[0][0]
                    if self.print_info: print('Two open dice are the same, bluffing for poker, since its possible')

                # Roll for 6s when they are not in the bid and can still be rolled
                elif 6 not in self.current_bid:  # if there is no 6 in the current bid, another die can be rolled
                    if self.print_info: print('Rolling for a higher value')
                    self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][1], self.print_info)
                    dicecopy[1][1] = 1
                    if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                                know1=self.players[0].knowledge,
                                                                know2=self.players[1].knowledge,
                                                                know3=self.players[2].knowledge, turn=self.turn,
                                                                penal1=self.players[0].penalty_points,
                                                                penal2=self.players[1].penalty_points,
                                                                penal3=self.players[2].penalty_points,
                                                                losername=self.loser_name,
                                                                current_bid=self.current_bid, text='',
                                                                printtext=self.gui_print)
                    if self.press_to_continue:
                        input("Press [Enter] to continue...\n")

                    if not self.bid_possible(
                            self.cup.dice):  # if the cup is still not higher than the bid, make decision whether to roll another die
                        if self.print_info: print('Rolling for a higher value (2)')
                        self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][0], self.print_info)
                        dicecopy[1][0] = 1
                        if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                                    know1=self.players[0].knowledge,
                                                                    know2=self.players[1].knowledge,
                                                                    know3=self.players[2].knowledge, turn=self.turn,
                                                                    penal1=self.players[0].penalty_points,
                                                                    penal2=self.players[1].penalty_points,
                                                                    penal3=self.players[2].penalty_points,
                                                                    losername=self.loser_name,
                                                                    current_bid=self.current_bid, text='',
                                                                    printtext=self.gui_print)
                        if self.press_to_continue:
                            input("Press [Enter] to continue...\n")

                    elif random.randint(1,
                                        100) < 50:  # a higher bid is already obtained, but last dice might still be rolled to get a 6 #TODO: maybe work out probability
                        if self.print_info: print(
                            f'[ROLL] Cup is already higher, but Player is trying to roll {dicecopy[0][0]} to a higher value')
                        self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][0], self.print_info)
                        dicecopy[1][0] = 1
                        if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                                    know1=self.players[0].knowledge,
                                                                    know2=self.players[1].knowledge,
                                                                    know3=self.players[2].knowledge, turn=self.turn,
                                                                    penal1=self.players[0].penalty_points,
                                                                    penal2=self.players[1].penalty_points,
                                                                    penal3=self.players[2].penalty_points,
                                                                    losername=self.loser_name,
                                                                    current_bid=self.current_bid, text='',
                                                                    printtext=self.gui_print)

                # otherwise maybe roll, or maybe bluff, depending on the value of the remaining dice
                else:  # there is at least a 6 in the bid, now there are 2 possibilities:
                    if self.current_bid.count(6) == 1:  # there is only one 6 in the bid (must be the first)
                        # implement a chance to roll the other dice, otherwise go to bid phase and bluff
                        if random.randint(1, 1000) > (
                                1000 * dicecopy[0][1] / 6):  # a lower dice value has a higher chance to be thrown
                            if self.print_info: print(f'[ROLL] Trying to roll {dicecopy[0][1]} to a higher value')
                            self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(dicecopy[0][1], self.print_info)
                            dicecopy[1][1] = 1
                            if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=[],
                                                                        know1=self.players[0].knowledge,
                                                                        know2=self.players[1].knowledge,
                                                                        know3=self.players[2].knowledge, turn=self.turn,
                                                                        penal1=self.players[0].penalty_points,
                                                                        penal2=self.players[1].penalty_points,
                                                                        penal3=self.players[2].penalty_points,
                                                                        losername=self.loser_name,
                                                                        current_bid=self.current_bid, text='',
                                                                        printtext=self.gui_print)
                        else:
                            if self.print_info: print(
                                f'Player thinks bluffing with the dice open is less risky than to roll {dicecopy[0][1]}')

                    elif dicecopy[0][0] == dicecopy[0][
                        0] == 6:  # otherwise both unrolled dice are 6, a bluff will be made in bidding phase on the basis of knowledge
                        self.players[self.turn].bluff_poker = True
                        self.players[self.turn].bluff_value = dicecopy[0][0]


        # if self.print_info: print(dicecopy)
        self.public_knowledge = []

        for i in range(3):
            if dicecopy[1][i] == 0:
                value = dicecopy[0][i]
                # if self.print_info: print(f'value = {value}')
                self.public_knowledge.append(value)

        self.gui_print += f'\nCommon knowledge (non-rolled dice): {self.public_knowledge}'
        if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=self.public_knowledge,
                                                    know1=self.players[0].knowledge,
                                                    know2=self.players[1].knowledge,
                                                    know3=self.players[2].knowledge, turn=self.turn,
                                                    penal1=self.players[0].penalty_points,
                                                    penal2=self.players[1].penalty_points,
                                                    penal3=self.players[2].penalty_points,
                                                    losername=self.loser_name,
                                                    current_bid=self.current_bid, text='',
                                                    printtext=self.gui_print)

    def roll_poker(self, threshold):
        to_roll = []

        # Poker is rolled
        if is_poker(self.cup.dice):
            if self.cup.dice[0] > threshold:
                if self.print_info: print('Poker beaten')
                self.penalise_poker(2)
            elif self.cup.dice[0] == threshold:
                if self.print_info: print('Poker equalled')
                self.penalise_poker(1)
            else:
                if self.print_info: print('Poker rolled, but not high enough. rolling all again.')
                to_roll.extend([0, 1, 2])

        # Highest dice are equal
        elif self.cup.dice[0] == self.cup.dice[1]:
            if self.cup.dice[0] >= threshold:
                if self.print_info: print('Equal dice with value high enough, rolling dice 2 again.')
                to_roll.append(2)
            elif self.cup.dice[2] >= threshold:
                if self.print_info: print('Equal dice with value NOT high enough, but lowest is. rolling 0, 1 again.')
                to_roll.extend([0, 1])
            else:
                if self.print_info: print('Equal dice with value NOT high enough, rolling all again.')
                to_roll.extend([0, 1, 2])

        # Lowest dice are equal
        elif self.cup.dice[1] == self.cup.dice[2]:
            if self.cup.dice[1] >= threshold:
                if self.print_info: print('Equal dice with value high enough, rolling dice 0 again.')
                to_roll.append(0)
            elif self.cup.dice[0] >= threshold:
                if self.print_info: print('Equal dice with value NOT high enough, but highest is. rolling 1, 2 again.')
                to_roll.extend([1, 2])
            else:
                if self.print_info: print('Equal dice with value NOT high enough, rolling all again.')
                to_roll.extend([0, 1, 2])

        # No dice are equal
        elif self.cup.dice[0] >= threshold:
            if self.print_info: print('Highest dice beats threshold, rolling dice 1 and dice 2 again.')
            to_roll.extend([1, 2])
        else:
            if self.print_info: print('No die was high enough, rolling all dice again.')
            to_roll.extend([0, 1, 2])

        return to_roll

    def penalise_poker(self, outcome):
        won = 2
        equal = 1
        lost = 0

        if self.print_info: print(f'[PENALISE POKER] The poker was {self.current_bid} and the cup has {self.cup.dice}')
        if outcome == won:
            self.players[(self.turn + self.n_players - 1) % self.n_players].penalty_points += 1
            if self.print_info: print(
                f'Player {self.turn} has rolled a higher poker! Player {(self.turn + self.n_players - 1) % self.n_players} gets one penalty point')
            self.turn = (self.turn + self.n_players - 1) % self.n_players  # previous player can start again
        elif outcome == equal:
            if self.print_info: print(f'Player {self.turn} has rolled the same poker! No player gets a penalty point.')
        elif outcome == lost:
            self.players[self.turn].penalty_points += 1
            if self.print_info: print(f'Player {self.turn} did not roll high enough and gets one penalty point.')

    def bidding(self, strategy):
        if strategy == 'truthful':
            if self.bid_possible(self.cup.dice):
                self.current_bid = copy(self.cup.dice)
                # if self.print_info: print('[DEBUG] copy the values')
            else:
                random_add = random.randint(1, self.max_overbid)
                if (AllPossibleWorlds.index(self.current_bid) + random_add) < 56:
                    self.current_bid = AllPossibleWorlds[
                        AllPossibleWorlds.index(
                            self.current_bid) + random_add]  # bid slightly higher than previous player

                elif (AllPossibleWorlds.index(self.current_bid) + 1) < 56:
                    self.current_bid = AllPossibleWorlds[
                        AllPossibleWorlds.index(self.current_bid) + 1]  # bid slightly higher than previous player


        elif strategy == 'always_overbid':
            random_add = random.randint(1, self.max_overbid)
            if (AllPossibleWorlds.index(self.current_bid) + random_add) < 56:
                self.current_bid = AllPossibleWorlds[
                    AllPossibleWorlds.index(self.current_bid) + random_add]  # bid slightly higher than previous player

            elif (AllPossibleWorlds.index(self.current_bid) + 1) < 56:
                self.current_bid = AllPossibleWorlds[
                    AllPossibleWorlds.index(self.current_bid) + 1]  # bid slightly higher than previous player

        elif strategy == 'knowledge_based':
            # The knowledge agent bids truthfully given that it rolled high enough or bluffs giving the most believable lie with a high enough value.
            if self.bid_possible(self.cup.dice):  # bid truthful if possible
                self.current_bid = copy(self.cup.dice)

            elif self.players[self.turn].bluff_poker:  # decided to bluff at rolling phase
                self.current_bid = [self.players[self.turn].bluff_value] * 3
                self.players[self.turn].bluff_poker = False
            else:  # truthful bet impossible, look for a smart bluff

                # determine the possible bets for the next player (now implemented for all players), when bluffing
                if len(self.public_knowledge) == 0:  # no visible dice means all are unknown
                    possible_bets = AllPossibleWorlds
                elif len(self.public_knowledge) == 1:  # one dice visible
                    pk1 = self.public_knowledge[0]
                    possible_bets = [s for s in AllPossibleWorlds if pk1 in s]
                else:  # two dice visible
                    pk1, pk2 = self.public_knowledge
                    if pk1 != pk2:
                        possible_bets = [s for s in AllPossibleWorlds if (pk1 in s and pk2 in s)]
                    else:
                        possible_bets = list(s for s in AllPossibleWorlds if s.count(
                            pk1) >= 2)  # all instances of possible worlds with two dice of the same kind

                higher_possible = [w for w in possible_bets if
                                   AllPossibleWorlds.index(w) > AllPossibleWorlds.index(self.current_bid)]
                if self.print_info: print(f'possible bluffs:{higher_possible}')
                if len(higher_possible) != 0:  # there is at least one higher possible world for bluffing
                    # create some randomness in bluffing
                    if len(higher_possible) > 2:
                        random_higher = random.randint(0, 2)
                        self.current_bid = higher_possible[random_higher]
                    elif len(higher_possible) > 1:
                        random_higher = random.randint(0, 1)
                        self.current_bid = higher_possible[random_higher]
                    else:
                        self.current_bid = higher_possible[0]
                else:  # there is no possible bluff
                    if (AllPossibleWorlds.index(self.current_bid) + 1) < 56:
                        self.current_bid = AllPossibleWorlds[
                            AllPossibleWorlds.index(self.current_bid) + 1]  # bid slightly higher than previous player

    def penalise(self):
        if self.print_info: print(f'[PENALISE] The bid was {self.current_bid} and the cup has {self.cup.dice}')
        if AllPossibleWorlds.index(self.current_bid) > AllPossibleWorlds.index(
                self.cup.dice):  # the bid was higher than the cup, previous player was bluffing/lying
            self.players[(self.turn + self.n_players - 1) % self.n_players].penalty_points += 1
            if self.print_info: print(
                f'Player {self.turn} was right, Player {(self.turn + self.n_players - 1) % self.n_players} gets one penalty point')
            self.turn = (self.turn + self.n_players - 1) % self.n_players  # previous player can start again
        else:
            self.players[self.turn].penalty_points += 1
            if self.print_info: print(f'Player {self.turn} was wrong and gets one penalty point')
            # turn remains with this player
        self.gui_print += f'\n[PENALISE] The bid was {self.current_bid} and the cup has {self.cup.dice}\nPlayer {self.turn} was wrong and gets one penalty point'
        if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=self.public_knowledge,
                                                    know1=self.players[0].knowledge,
                                                    know2=self.players[1].knowledge,
                                                    know3=self.players[2].knowledge, turn=self.turn,
                                                    penal1=self.players[0].penalty_points,
                                                    penal2=self.players[1].penalty_points,
                                                    penal3=self.players[2].penalty_points,
                                                    losername=self.loser_name,
                                                    current_bid=self.current_bid, text='', printtext=self.gui_print)

    def update_knowledge(self):
        if self.print_info: print(f'Open dice are: {self.public_knowledge}')
        for i in range(self.n_players):
            if i == self.turn:
                self.players[i].knowledge = [self.cup.dice]
            else:
                if len(self.public_knowledge) == 0:  # no visible dice means all are unknown
                    self.players[i].knowledge = AllPossibleWorlds
                elif len(self.public_knowledge) == 1:  # one dice visible
                    pk1 = self.public_knowledge[0]
                    self.players[i].knowledge = [s for s in AllPossibleWorlds if pk1 in s]
                elif len(self.public_knowledge) == 2:  # two dice visible
                    pk1, pk2 = self.public_knowledge
                    if pk1 != pk2:
                        self.players[i].knowledge = [s for s in AllPossibleWorlds if (pk1 in s and pk2 in s)]
                    else:
                        self.players[i].knowledge = list(s for s in AllPossibleWorlds if s.count(
                            pk1) >= 2)  # all instances of possible worlds with two dice of the same kind
            # if self.print_info: Printing knowledge of agents :
            # if self.print_info: print(
            #     f'Player {i} knowledge (Number of possible worlds = {len(self.players[i].knowledge)}): {self.players[i].knowledge}')
            # # if self.print_info: print(self.players[i].knowledge)
            higher_possible = [w for w in self.players[i].knowledge if
                               AllPossibleWorlds.index(w) > AllPossibleWorlds.index(self.current_bid)]
            # if self.print_info: print(f'of which the following are higher than current bid ({len(higher_possible)}): {higher_possible}')

    # Main loop that plays the game
    def play(self):
        while not self.end_game:
            # start_visuals()
            if self.state == states['start']:  # first turn is different than other turns,
                if self.print_info: print('------------ NEW ROUND --------------')
                if self.print_info: print(f'[STARTING TURN] of Player {self.turn}')
                self.gui_print = ''
                self.gui_print += f'[STARTING TURN] of Player {self.turn + 1}'


                # self.cup.roll_all()
                self.first_turn = True  # might be used in belief probability
                self.public_knowledge.clear()
                # self.cup.dice = [6, 6, 2]
                self.cup.roll_all()

                self.gui_print += f"\n[STARTING ROLL] Player {self.turn + 1} rolls the dice and rolls {self.cup.dice}"
                print(self.gui_print)
                if self.print_info: print(f"[STARTING ROLL] Player {self.turn + 1} rolls the dice and rolls:")
                if self.print_info: print_dice(self.cup.dice)

                if self.players[self.turn].bid_strategy == 'truthful':
                    self.current_bid = copy(self.cup.dice)
                elif self.players[self.turn].bid_strategy == 'knowledge_based':
                    self.current_bid = copy(self.cup.dice)
                else:
                    self.current_bid = random_bid_return()  # random bid

                self.update_knowledge()
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=self.public_knowledge,
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid='', text='',
                                                            printtext=self.gui_print)

                self.gui_print += f"\n[STARTING BID] Player {self.turn + 1} bids: {self.current_bid}"
                if self.print_info: print(f"[STARTING BID] Player {self.turn} bids: {self.current_bid}")
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice,
                                                            public_knowledge=self.public_knowledge,
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)
                self.update_turn()
                self.state = states['believe/call_bluff_phase']


                self.gui_print += f'\nPlayer {self.turn+1} has to believe or call the bluff'
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=self.public_knowledge,
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)
                continue

            if self.state == states['poker_phase']:
                threshold = self.current_bid[0]
                to_roll = []

                if self.print_info: print(
                    f'[POKER PHASE] Player {self.turn} has three rolls to try and equal or beat {self.current_bid}.')
                self.cup.roll_all()
                if self.print_info: print(f'[ROLL 1] Player {self.turn} rolls the dice and rolls:')
                if self.print_info: print_dice(self.cup.dice)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                to_roll = self.roll_poker(threshold)

                if self.print_info: print(f'[ROLL 2]')
                for d in to_roll:
                    if self.print_info: print(f'Rolling dice {d}:')
                    self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(self.cup.dice[d], self.print_info)
                if self.print_info: print_dice(self.cup.dice)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                to_roll = self.roll_poker(threshold)

                if self.print_info: print(f'[ROLL 3]')
                for d in to_roll:
                    if self.print_info: print(f'Rolling dice {d}:')
                    self.gui_print += f'\nPlayer {self.turn + 1} '+ self.cup.roll_dice_with_value(self.cup.dice[d], self.print_info)
                if self.print_info: print_dice(self.cup.dice)

                if is_poker(self.cup.dice) and self.cup.dice[0] > threshold:
                    self.penalise_poker(2)
                elif is_poker(self.cup.dice) and self.cup.dice[0] == threshold:
                    self.penalise_poker(1)
                else:
                    self.penalise_poker(0)

                self.gui_print += f"\n[SCORE] is now as follows:"
                if self.print_info: print('[SCORE] is now as follows:', end=" ")
                for i in range(self.n_players):  # check if a player has lost (i.e has the max penalty points)
                    self.gui_print += f"\nPlayer {i}: {self.players[i].penalty_points} points: "
                    if self.print_info: print(f'Player {i}: {self.players[i].penalty_points} points: ', end=" ")
                    if self.print_info: print_string = [self.loser_name[j] for j in
                                                        range(self.players[i].penalty_points)]
                    if self.print_info: print("".join(print_string), end=" ")
                    self.gui_print += "\n" + "".join([self.loser_name[j] for j in
                                                      range(self.players[i].penalty_points)])

                if self.print_info: print()  # if self.print_info: print for new line
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=self.public_knowledge,
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)

                for i in range(self.n_players):  # check if a player has lost (i.e has the max penalty points)
                    if self.players[i].penalty_points == self.max_penalty:

                        if self.print_info: print(
                            f'Player {i} has {self.max_penalty} penalty points and has lost the game!')
                        self.gui_print += f'\nPlayer {i} has {self.max_penalty} penalty points and has lost the game!'
                        if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=self.public_knowledge,
                                                                    know1=self.players[0].knowledge,
                                                                    know2=self.players[1].knowledge,
                                                                    know3=self.players[2].knowledge, turn=self.turn,
                                                                    penal1=self.players[0].penalty_points,
                                                                    penal2=self.players[1].penalty_points,
                                                                    penal3=self.players[2].penalty_points,
                                                                    losername=self.loser_name,
                                                                    current_bid=self.current_bid, text='',
                                                                    printtext=self.gui_print)
                        self.players[i].losses += 1
                        losscount[i] += 1
                        self.end_game = True
                        break

                if not self.end_game:
                    if self.press_to_continue:
                        input("Press [Enter] to continue...\n")
                self.state = states['start']
                continue

            if self.state == states['penalty_phase']:
                self.penalise()

                self.gui_print += f"\n[SCORE] is now as follows:"
                if self.print_info: print('[SCORE] is now as follows:', end=" ")
                for i in range(self.n_players):  # check if a player has lost (i.e has the max penalty points)
                    # self.gui_print += f"\nPlayer {i}: {self.players[i].penalty_points} points: "
                    if self.print_info: print(f'Player {i}: {self.players[i].penalty_points} points: ', end=" ")
                    if self.print_info: print_string = [self.loser_name[j] for j in
                                                        range(self.players[i].penalty_points)]
                    if self.print_info: print("".join(print_string), end=" ")
                    self.gui_print += f"\nPlayer {i}: {self.players[i].penalty_points} points: " + "".join(
                        [self.loser_name[j] for j in
                         range(self.players[i].penalty_points)])
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=self.public_knowledge,
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)

                for i in range(self.n_players):  # check if a player has lost (i.e has the max penalty points)
                    if self.players[i].penalty_points == self.max_penalty:
                        if self.print_info: print(
                            f'Player {i} has {self.max_penalty} penalty points and has lost the game!')
                        self.gui_print += f'\nPlayer {i} has {self.max_penalty} penalty points and has lost the game!'
                        if self.visualise_game_gui: Visualized_game(cup=self.cup.dice,
                                                                    public_knowledge=self.public_knowledge,
                                                                    know1=self.players[0].knowledge,
                                                                    know2=self.players[1].knowledge,
                                                                    know3=self.players[2].knowledge, turn=self.turn,
                                                                    penal1=self.players[0].penalty_points,
                                                                    penal2=self.players[1].penalty_points,
                                                                    penal3=self.players[2].penalty_points,
                                                                    losername=self.loser_name,
                                                                    current_bid=self.current_bid, text='',
                                                                    printtext=self.gui_print)
                        self.players[i].losses += 1
                        losscount[i] += 1
                        self.end_game = True
                        break

                if not self.end_game:
                    if self.press_to_continue:
                        input("Press [Enter] to continue...\n")
                self.state = states['start']
                continue

                # ------------- These states are looped within one round --------------

            if self.state == states['believe/call_bluff_phase']:

                if self.print_info: print(f'[TURN] of Player {self.turn}')
                if self.determine_bluff(
                        self.players[self.turn].determine_bluff_strategy):  # if true, then agent believes it is a bluff
                    self.gui_print += f"\nPlayer {self.turn + 1} does not believe Player {(self.turn + self.n_players - 1) % self.n_players + 1} (i.e. {self.current_bid} is not under the cup)'"
                    if self.print_info: print(
                        f'Player {self.turn} does not believe Player {(self.turn + self.n_players - 1) % self.n_players} (i.e. {self.current_bid} is not under the cup)')
                    self.state = states['penalty_phase']
                    if self.visualise_game_gui: Visualized_game(cup=self.cup.dice,
                                                                public_knowledge=self.public_knowledge,
                                                                know1=self.players[0].knowledge,
                                                                know2=self.players[1].knowledge,
                                                                know3=self.players[2].knowledge, turn=self.turn,
                                                                penal1=self.players[0].penalty_points,
                                                                penal2=self.players[1].penalty_points,
                                                                penal3=self.players[2].penalty_points,
                                                                losername=self.loser_name,
                                                                current_bid=self.current_bid, text='Bluff!',
                                                                printtext=self.gui_print)

                else:
                    if self.print_info: print(
                        f'Player {self.turn + 1} believes Player {(self.turn + self.n_players - 1) % self.n_players} (i.e. that at least {self.current_bid} is  under the cup)')
                    self.gui_print += f"\nPlayer {self.turn + 1} believes Player {(self.turn + self.n_players - 1) % self.n_players + 1} (i.e. that at least {self.current_bid} is  under the cup)"
                    self.players[self.turn].knowledge = self.cup.dice
                    if self.visualise_game_gui: Visualized_game(cup=self.cup.dice,
                                                                public_knowledge=self.public_knowledge,
                                                                know1=self.players[0].knowledge,
                                                                know2=self.players[1].knowledge,
                                                                know3=self.players[2].knowledge, turn=self.turn,
                                                                penal1=self.players[0].penalty_points,
                                                                penal2=self.players[1].penalty_points,
                                                                penal3=self.players[2].penalty_points,
                                                                losername=self.loser_name,
                                                                current_bid=self.current_bid, text='Believe!',
                                                                printtext=self.gui_print)

                    if is_poker(self.current_bid):
                        self.state = states['poker_phase']
                    else:
                        self.state = states['roll_dice_phase']
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                continue

            if self.state == states['roll_dice_phase']:
                self.roll_dice(self.players[self.turn].roll_strategy)
                if self.print_info: print(f'Player {self.turn} has rolled the dice, the cup is now as follows:')
                self.gui_print += f'\nPlayer {self.turn + 1} has rolled the dice, the cup is now: {self.cup.dice}'
                if self.print_info: print_dice(self.cup.dice)
                self.update_knowledge()
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=self.public_knowledge,
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)

                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                self.state = states['bidding_phase']
                continue

            if self.state == states['bidding_phase']:
                self.bidding(self.players[self.turn].bid_strategy)
                if self.print_info: print(f'Player {self.turn} has bid: {self.current_bid}')
                self.gui_print += f'\nPlayer {self.turn +1} has bid: {self.current_bid}'
                if self.visualise_game_gui: Visualized_game(cup=self.cup.dice, public_knowledge=self.public_knowledge,
                                                            know1=self.players[0].knowledge,
                                                            know2=self.players[1].knowledge,
                                                            know3=self.players[2].knowledge, turn=self.turn,
                                                            penal1=self.players[0].penalty_points,
                                                            penal2=self.players[1].penalty_points,
                                                            penal3=self.players[2].penalty_points,
                                                            losername=self.loser_name,
                                                            current_bid=self.current_bid, text='',
                                                            printtext=self.gui_print)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                self.update_turn()
                self.state = states['believe/call_bluff_phase']
                continue
        if self.print_info: print('Game finished!')
