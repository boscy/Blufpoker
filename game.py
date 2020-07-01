from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import colors
import random
import numpy as np
import seaborn as sns

from gui import GUI
from player import Player
from cup import Cup
from copy import copy, deepcopy

#a copy for if we want the old game back

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

## GUI variables

bg_colour = "#0D865D"
info_colour = 'gray'
kn_colour = 'white'
db_colour = "#8B4513"

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
    def __init__(self, n_players=3, print_info = True, press_to_continue = True, visualize_gui = True, mean_th = 3/12):
        """
        Main function for initializing the game
        """
        self.players = [Player() for _ in range(n_players)]
        self.end_game = False
        self.first_turn = True
        self.current_bid = []
        self.public_knowledge = []
        self.n_players = n_players
        self.cup = Cup()
        self.turn = random.randint(0, n_players - 1)  # first turn is random
        self.state = states['start']
        self.loser_name = ['L', '0', 'Z', 'E', 'R']  # TODO make is such that user can set this.
        self.max_penalty = len(self.loser_name)
        self.max_overbid = 3
        self.believe_threshold_mean = mean_th

        self.visualize_gui = visualize_gui            
        self.print_info = print_info  #
        self.press_to_continue = press_to_continue

        ############# Agent strategies configuration ######################

        self.players[0].roll_strategy = 'random'
        self.players[0].bid_strategy = 'truthful'
        self.players[0].determine_bluff_strategy = 'random'

        # self.players[0].roll_strategy = 'greedy'
        # self.players[0].bid_strategy = 'always_overbid'
        # self.players[0].determine_bluff_strategy = 'always_true'
        #
        # self.players[1].roll_strategy = 'random'
        # self.players[1].bid_strategy = 'truthful'
        # self.players[1].determine_bluff_strategy = 'random'

        self.players[1].roll_strategy = 'greedy'
        self.players[1].bid_strategy = 'truthful'
        self.players[1].determine_bluff_strategy = 'always_true'

        self.players[2].roll_strategy = 'knowledge_based'
        self.players[2].bid_strategy = 'knowledge_based'
        self.players[2].determine_bluff_strategy = 'knowledge_based'

        if visualize_gui: 
            self.gui = GUI()

        # self.players[1].roll_strategy = 'knowledge_based'
        # self.players[1].bid_strategy = 'knowledge_based'
        # self.players[1].determine_bluff_strategy = 'knowledge_based'
        #
        # self.players[0].roll_strategy = 'knowledge_based'
        # self.players[0].bid_strategy = 'knowledge_based'
        # self.players[0].determine_bluff_strategy = 'knowledge_based'


    ## GUI Functions ----------------------------------------- ##

    def moveDiceBox(self,player):
        if player == 0: self.gui.diceBox.place(rely=0.57, relx = 0.1)
        elif player == 1: self.gui.diceBox.place(rely = 0.02, relx = 0.07)
        elif player == 2: self.gui.diceBox.place(rely=0.12, relx = 0.69)

    def writePenalty(self, player, string):
        penalty = Label(self.gui.penalties, text=string, bg=info_colour)
        if player == 0: penalty.grid(row = 3, column=3)
        elif player == 1: penalty.grid(row = 5, column=3)
        elif player == 2: penalty.grid(row = 7, column=3)
            
    def writeInfo(self, string):
        self.gui.gi_text.insert("1.0", string + "\n")

    def writeKnowledge(self, pw, cb):
        
        hW = [w for w in pw if AllPossibleWorlds.index(w) >= AllPossibleWorlds.index(self.current_bid)]
        if pw == hW:
            c = colors.ListedColormap([ 'green', 'silver'])
        else:
            c = colors.ListedColormap([ 'green', 'silver' ,'red'])

        plt.close('all')
        self.gui.chart.get_tk_widget().pack_forget()
        fig = plt.figure()
        data = np.zeros((7,8))

        for world in pw:
            val = (world[0]*100)+(world[1]*10)+world[2]
            for y in range(7):
                for x in range(8):
                    if self.gui.labels[y][x] == str(val):
                        data[y][x] = 1
                        if world == cb:
                            data[y][x] = -1

        for world in hW:
            val = (world[0]*100)+(world[1]*10)+world[2]
            for y in range(7):
                for x in range(8):
                    if self.gui.labels[y][x] == str(val):
                        data[y][x] = -1

        ax = sns.heatmap(data, annot=self.gui.labels, fmt='',xticklabels=False, yticklabels=False, cmap=c, cbar= False, linewidths=1, linecolor='white')
        fig.add_subplot(ax)

        self.gui.chart = FigureCanvasTkAgg(fig, self.gui.knowledge)
        self.gui.chart.get_tk_widget().pack(anchor=N)

        title = Label(self.gui.knowledge, text= "  Player 3 knowledge base  ")
        title.place(relx = 0.25, rely = 0.025)

        lbl1 = Label(self.gui.knowledge, text= "  Possible worlds higher or equal than current bid  ", bg='green', pady = 2, fg='white')
        lbl1.place(rely = 0.59, relx = 0.05)

        lbl2 = Label(self.gui.knowledge, text= "  Possible worlds lower than current bid  ", bg = 'red', pady = 2, fg='white')
        lbl2.place(rely = 0.63, relx = 0.05)

        lbl3 = Label(self.gui.knowledge, text= "    Impossible worlds    ", bg= 'silver', pady = 2)
        lbl3.place(rely = 0.67, relx = 0.05)

    def drawDice(self, d):
        d1 = d[0]-1
        d2 = d[1]-1
        d3 = d[2]-1

        self.gui.show_d1 = Label(self.gui.diceBox, image= self.gui.dice[d1])
        self.gui.show_d1.place(rely = 0.25, relx = 0.25)

        self.gui.show_d2 = Label(self.gui.diceBox, image = self.gui.dice[d2])
        self.gui.show_d2.place(rely = 0.25, relx = 0.55)

        self.gui.show_d3 = Label(self.gui.diceBox, image = self.gui.dice[d3])
        self.gui.show_d3.place(rely = 0.55, relx = 0.4)

    def removeDice(self):
        self.gui.show_d1.place_forget()
        self.gui.show_d2.place_forget()
        self.gui.show_d3.place_forget()

    def writeCurrentBid(self, bid):
        self.gui.currentBid = Button(self.gui.game, text= "Current bid: " + str(bid))
        self.gui.currentBid.place(relx = 0.4, rely = 0.5)

    def removeOpenDice(self):
        self.gui.openDie1.place_forget()
        self.gui.openDie2.place_forget()

    def showOpenDice(self, pk):
        self.removeOpenDice()

        if len(pk) == 1:
            self.gui.openDie1 = Label(self.gui.knowledge, image = self.gui.dice[pk[0]-1])
            self.gui.openDie1.place(relx = 0.05, rely = 0.9)
        elif len(pk) == 2:
            self.gui.openDie1 = Label(self.gui.knowledge, image = self.gui.dice[pk[0]-1])
            self.gui.openDie1.place(relx = 0.05, rely = 0.9)
            self.gui.openDie2 = Label(self.gui.knowledge, image = self.gui.dice[pk[1]-1])
            self.gui.openDie2.place(relx = 0.25, rely = 0.9)

    def clearKnowledge(self):
        plt.close('all')
        self.gui.chart.get_tk_widget().pack_forget()
        fig = plt.figure()
        data = np.zeros((7,8))
        c = colors.ListedColormap([ 'white'])
        ax = sns.heatmap(data, annot=self.gui.labels, fmt='',xticklabels=False, yticklabels=False, cmap=c, cbar= False, linewidths=1, linecolor='grey')
        fig.add_subplot(ax)

        self.gui.chart = FigureCanvasTkAgg(fig, self.gui.knowledge)
        self.gui.chart.get_tk_widget().pack(anchor=N)

        title = Label(self.gui.knowledge, text= "  Player 3 knowledge base  ")
        title.place(relx = 0.25, rely = 0.025)

        lbl1 = Label(self.gui.knowledge, text= "  Possible worlds higher or equal than current bid  ", bg='green', pady = 2, fg='white')
        lbl1.place(rely = 0.59, relx = 0.05)

        lbl2 = Label(self.gui.knowledge, text= "  Possible worlds lower than current bid  ", bg = 'red', pady = 2, fg='white')
        lbl2.place(rely = 0.63, relx = 0.05)

        lbl3 = Label(self.gui.knowledge, text= "    Impossible worlds    ", bg= 'silver', pady = 2)
        lbl3.place(rely = 0.67, relx = 0.05)

    ##-----------------------------------------------------------------##

    def update_turn(self):  # sets turn to the next player
        self.turn = (self.turn + 1) % self.n_players
        if self.visualize_gui: self.moveDiceBox(self.turn)
        

    def bid_possible(self, bid,prints=True):
        if AllPossibleWorlds.index(self.current_bid) < AllPossibleWorlds.index(bid):
            if prints:
                if self.visualize_gui: self.writeInfo(f'Truthful bid is possible, {bid} higher than {self.current_bid}')
            # self.if self.print_info: print_dice(bid)
            return True
        else:
            if self.visualize_gui: self.writeInfo(f'Truthful bid is impossible, {bid} not higher than {self.current_bid}')
            return False

    def determine_bluff(self, strategy):
        if strategy == 'random':
            believe_percentage = 80
            if random.randint(1, 100) > believe_percentage or (  # believing probability
                    AllPossibleWorlds.index(self.current_bid) == len(AllPossibleWorlds) - 1):
                return True
            else:
                return False

        elif strategy == 'always_believe':
            return False #never call bluff

        elif strategy == 'never_believe':
            return True #always call bluff

        elif strategy == 'knowledge_based':
            if self.current_bid not in self.players[self.turn].knowledge:
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
                if self.visualize_gui: self.writeInfo("Player 3 decision making process for believing / calling bluff...")
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                if self.print_info: print(
                    f'Probability of rolling possible higher worlds among possible worlds: {probability}')
                if self.visualize_gui: self.writeInfo(f'Probability of rolling possible higher worlds among possible worlds: {round(probability, 2)}')
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
                    if self.visualize_gui: self.writeInfo(f'Probability of bid: {round(probability, 2)} >= Believe Threshold: {round(believe_threshold[0], 2)}')
                    return False  # not a bluff -> believe
                else:
                    if self.print_info: print(f' {probability} < {believe_threshold}')
                    if self.visualize_gui: self.writeInfo(f'Probability of bid: {round(probability, 2)} < Believe Threshold: {round(believe_threshold[0], 2)}')
                    return True

    def roll_dice(self, roll_strategy):
        # dice are always ordered, so ranked from highest to lowest
        # maintain which dice are rolled, such that we can know what can be set as public knowledge
        dicecopy = [copy(self.cup.dice), [0, 0, 0]]  # make a copy of the dice and whether they are rolled

        # roll according to strategies 'random', '1_lowest', 'random_lowest' or 'greedy'
        if roll_strategy == 'random':
            if self.visualize_gui: self.writeInfo('[ROLL] Rolling random die')
            randomDie = random.randint(0, 2)
            rollprint = self.cup.roll_dice_with_value(dicecopy[0][randomDie],self.visualize_gui)
            if self.visualize_gui: self.writeInfo(rollprint)
            if self.press_to_continue:
                input("Press [Enter] to continue...\n")
            dicecopy[1][randomDie] = 1
            

        elif roll_strategy == '1_lowest':
            if self.visualize_gui: self.writeInfo('[ROLL] Rolling 1 lowest die ')
            rollprint = self.cup.roll_dice_with_value(dicecopy[0][2],self.visualize_gui)  # rolls the lowest die
            if self.visualize_gui: self.writeInfo(rollprint)
            if self.press_to_continue:
                input("Press [Enter] to continue...\n")
            dicecopy[1][2] = 1

        elif roll_strategy == 'random_lowest':
            if self.visualize_gui: self.writeInfo('[ROLL] Rolling random n lowest dice') # rolls the n lowest dice, with n randomly determined
            random_n = random.randint(0, 2)
            rollprint = self.cup.roll_dice_with_value(dicecopy[0][2],self.visualize_gui)
            if self.visualize_gui: self.writeInfo(rollprint)
            if self.press_to_continue:
                input("Press [Enter] to continue...\n")
            dicecopy[1][2] = 1
            if random_n > 0:  # must be done dice by dice since reshuffle disallows a loop
                rollprint = self.cup.roll_dice_with_value(dicecopy[0][1],self.visualize_gui)
                if self.visualize_gui: self.writeInfo(rollprint)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                dicecopy[1][1] = 1
            if random_n > 1:
                rollprint = self.cup.roll_dice_with_value(dicecopy[0][0],self.visualize_gui)
                if self.visualize_gui: self.writeInfo(rollprint)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                dicecopy[1][0] = 1

        elif roll_strategy == 'greedy':  # rolls all dice that aren't 6's
            if dicecopy[0][0] ==  dicecopy[0][1] == dicecopy[0][2] == 6: #all dice are 6s, roll the lowest
                rollprint = self.cup.roll_dice_with_value(dicecopy[0][0], self.visualize_gui)
                if self.visualize_gui: self.writeInfo(rollprint)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
            else:
                if self.visualize_gui: self.writeInfo('[ROLL] Rolling greedy (all non-6 dice)')
                if dicecopy[0][0] != 6:
                    rollprint = self.cup.roll_dice_with_value(dicecopy[0][0],self.visualize_gui)
                    if self.visualize_gui: self.writeInfo(rollprint)
                    dicecopy[1][0] = 1
                if dicecopy[0][1] != 6:
                    rollprint = self.cup.roll_dice_with_value(dicecopy[0][1],self.visualize_gui)

                    if self.visualize_gui: self.writeInfo(rollprint)
                    dicecopy[1][1] = 1
                if dicecopy[0][2] != 6:
                    rollprint = self.cup.roll_dice_with_value(dicecopy[0][2],self.visualize_gui)

                    if self.visualize_gui: self.writeInfo(rollprint)
                    dicecopy[1][2] = 1

        elif roll_strategy == 'knowledge_based':
            # Knowledge based rolling strategy

            rollprint = self.cup.roll_dice_with_value(dicecopy[0][
                                              2],self.visualize_gui)  # always rolls the lowest die first, this always has the highest chance of getting to a higher bet
            if self.visualize_gui: self.writeInfo(rollprint)
            dicecopy[1][2] = 1

            if not self.bid_possible(
                    self.cup.dice, prints=False):  # if the cup is not higher than the bid, make decision whether to roll another die or bluff
                if self.visualize_gui: self.writeInfo('First roll did not cause for a higher value than the current bid')
                if self.visualize_gui: self.drawDice(self.cup.dice)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                # implement small chance (1/6) of bluffing on poker in bidding round, if two dice can be displayed
                if dicecopy[0][0] == dicecopy[0][1] and random.randint(0, 1000) < 167:  # first two dice are the same
                    self.players[self.turn].bluff_poker = True
                    self.players[self.turn].bluff_value = dicecopy[0][0]
                    if self.visualize_gui: self.writeInfo('Two open dice are the same, bluffing for poker, since its possible')

                # Roll for 6s when they are not in the bid and can still be rolled
                elif 6 not in self.current_bid:  # if there is no 6 in the current bid, another die can be rolled
                    if self.visualize_gui: self.writeInfo('Rolling for a higher value')
                    rollprint = self.cup.roll_dice_with_value(dicecopy[0][1],self.visualize_gui)
                    if self.visualize_gui: self.writeInfo(rollprint)

                    dicecopy[1][1] = 1
                    if self.visualize_gui: self.drawDice(self.cup.dice)
                    if self.press_to_continue:
                        input("Press [Enter] to continue...\n")

                    if not self.bid_possible(
                            self.cup.dice):  # if the cup is still not higher than the bid, make decision whether to roll another die
                        if self.visualize_gui: self.writeInfo('Rolling for a higher value (2)')
                        rollprint = self.cup.roll_dice_with_value(dicecopy[0][0],self.visualize_gui)
                        if self.visualize_gui: self.writeInfo(rollprint)
                        dicecopy[1][0] = 1
                        if self.visualize_gui: self.drawDice(self.cup.dice)
                        if self.press_to_continue:
                            input("Press [Enter] to continue...\n")

                    elif random.randint(1,
                                        100) < 50:  # a higher bid is already obtained, but last dice might still be rolled to get a 6 #TODO: maybe work out probability
                        if self.visualize_gui: self.writeInfo(
                            f'[ROLL] Cup is already higher, player tries rolling {dicecopy[0][0]} to higher value')
                        rollprint = self.cup.roll_dice_with_value(dicecopy[0][0],self.visualize_gui)
                        if self.visualize_gui: self.writeInfo(rollprint)
                        dicecopy[1][0] = 1
                        if self.visualize_gui: self.drawDice(self.cup.dice)


                # otherwise maybe roll, or maybe bluff, depending on the value of the remaining dice
                else:  # there is at least a 6 in the bid, now there are 2 possibilities:
                    if self.current_bid.count(6) == 1:  # there is only one 6 in the bid (must be the first)
                        # implement a chance to roll the other dice, otherwise go to bid phase and bluff
                        if random.randint(1, 1000) > (
                                1000 * dicecopy[0][1] / 6):  # a lower dice value has a higher chance to be thrown
                            if self.visualize_gui: self.writeInfo(f'[ROLL] Trying to roll {dicecopy[0][1]} to a higher value')
                            rollprint = self.cup.roll_dice_with_value(dicecopy[0][1],self.visualize_gui)
                            if self.visualize_gui: self.writeInfo(rollprint)
                            if self.press_to_continue:
                                input("Press [Enter] to continue...\n")
                            dicecopy[1][1] = 1
                        else:
                            if self.visualize_gui: self.writeInfo(
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

        # if self.visualize_gui: 
        #     if len(self.public_knowledge != 0):
        #         self.showOpenDice(self.public_knowledge)

    def roll_poker(self, threshold):
        to_roll = []

        # Poker is rolled
        if is_poker(self.cup.dice):
            if self.cup.dice[0] > threshold:
                if self.visualize_gui: self.writeInfo('Poker beaten')
                self.penalise_poker(2)
            elif self.cup.dice[0] == threshold:
                if self.visualize_gui: self.writeInfo('Poker equalled')
                self.penalise_poker(1)
            else:
                if self.visualize_gui: self.writeInfo('Poker rolled, but not high enough. rolling all again.')
                to_roll.extend([0, 1, 2])

        # Highest dice are equal
        elif self.cup.dice[0] == self.cup.dice[1]:
            if self.cup.dice[0] >= threshold:
                if self.visualize_gui: self.writeInfo('Equal dice with value high enough, rolling dice 2 again.')
                to_roll.append(2)
            elif self.cup.dice[2] >= threshold:
                if self.visualize_gui: self.writeInfo('Equal dice with value NOT high enough, but lowest is. rolling 0, 1 again.')
                to_roll.extend([0, 1])
            else:
                if self.visualize_gui: self.writeInfo('Equal dice with value NOT high enough, rolling all again.')
                to_roll.extend([0, 1, 2])

        # Lowest dice are equal
        elif self.cup.dice[1] == self.cup.dice[2]:
            if self.cup.dice[1] >= threshold:
                if self.visualize_gui: self.writeInfo('Equal dice with value high enough, rolling dice 0 again.')
                to_roll.append(0)
            elif self.cup.dice[0] >= threshold:
                if self.visualize_gui: self.writeInfo('Equal dice with value NOT high enough, but highest is. rolling 1, 2 again.')
                to_roll.extend([1, 2])
            else:
                if self.visualize_gui: self.writeInfo('Equal dice with value NOT high enough, rolling all again.')
                to_roll.extend([0, 1, 2])

        # No dice are equal
        elif self.cup.dice[0] >= threshold:
            if self.visualize_gui: self.writeInfo('Highest dice beats threshold, rolling dice 1 and dice 2 again.')
            to_roll.extend([1, 2])
        else:
            if self.visualize_gui: self.writeInfo('No die was high enough, rolling all dice again.')
            to_roll.extend([0, 1, 2])

        return to_roll

    def penalise_poker(self, outcome):
        won = 2
        equal = 1
        lost = 0

        if self.visualize_gui: self.writeInfo(f'[PENALISE POKER] The poker was {self.current_bid} and the cup has {self.cup.dice}')
        if outcome == won:
            self.players[(self.turn + self.n_players - 1) % self.n_players].penalty_points += 1
            if self.visualize_gui: self.writeInfo(
                f'Player {self.turn +1} has rolled a higher poker! Player {(self.turn + self.n_players - 1) % self.n_players +1} gets one penalty point')
            self.turn = (self.turn + self.n_players - 1) % self.n_players  # previous player can start again
        elif outcome == equal:
            if self.visualize_gui: self.writeInfo(f'Player {self.turn +1} has rolled the same poker! No player gets a penalty point.')
        elif outcome == lost:
            self.players[self.turn].penalty_points += 1
            if self.visualize_gui: self.writeInfo(f'Player {self.turn +1} did not roll high enough and gets one penalty point.')
        
        for i in range(self.n_players):
            penalty = self.loser_name[:self.players[i].penalty_points]
            if self.visualize_gui: self.writePenalty(i, penalty)
        # if self.visualize_gui: self.removeDice()

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
                if self.print_info: print(f'possible bluffs ({len(higher_possible)}):{higher_possible}')
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
        if self.visualize_gui: self.writeCurrentBid(self.current_bid)

    def penalise(self):
        if self.visualize_gui: self.writeInfo(f'[PENALISE] The bid was {self.current_bid} and the cup has {self.cup.dice}')
        if AllPossibleWorlds.index(self.current_bid) > AllPossibleWorlds.index(
                self.cup.dice):  # the bid was higher than the cup, previous player was bluffing/lying
            self.players[(self.turn + self.n_players - 1) % self.n_players].penalty_points += 1
            if self.visualize_gui: self.writeInfo(
                f'Player {self.turn +1} was right, Player {(self.turn + self.n_players - 1) % self.n_players +1} gets one penalty point')
            self.turn = (self.turn + self.n_players - 1) % self.n_players  # previous player can start again
        else:
            self.players[self.turn].penalty_points += 1
            if self.visualize_gui: self.writeInfo(f'Player {self.turn +1} was wrong and gets one penalty point')
            # turn remains with this player
        # if self.visualize_gui: self.removeDice()

    def update_knowledge(self):
        if self.print_info: print(f'Open dice are: {self.public_knowledge}')
        if self.visualize_gui: self.showOpenDice(self.public_knowledge)

        
        # if self.visualize_gui: 
        #     if len(self.public_knowledge != 0): self.showOpenDice(self.public_knowledge)
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
                higher_possible = [w for w in self.players[i].knowledge if
                               AllPossibleWorlds.index(w) > AllPossibleWorlds.index(self.current_bid)]            
                if self.visualize_gui: self.writeKnowledge(self.players[i].knowledge, self.current_bid)

            
            if self.print_info: print(
                f'Player {i +1} knowledge (Number of possible worlds = {len(self.players[i].knowledge)}): {self.players[i].knowledge}')
            # if self.print_info: print(self.players[i].knowledge)
            higher_possible = [w for w in self.players[i].knowledge if
                               AllPossibleWorlds.index(w) > AllPossibleWorlds.index(self.current_bid)]
            # if self.print_info: print(f'of which the following are higher than current bid ({len(higher_possible)}): {higher_possible}\n')


## ----------------------------------------------------------------- ##

    # Main loop that plays the game
    def play(self):

        while not self.end_game:
            if self.state == states['start']:  # first turn is different than other turns,
                if self.visualize_gui: self.moveDiceBox(self.turn)
                if self.visualize_gui: self.removeDice()
                if self.visualize_gui: self.writeInfo('------------ NEW ROUND --------------')
                if self.visualize_gui: self.writeInfo(f'[STARTING TURN] of Player {self.turn +1}')
                if self.visualize_gui: self.clearKnowledge()
                
                # self.cup.roll_all()
                self.first_turn = True  # might be used in belief probability
                self.public_knowledge.clear()
                # self.cup.dice = [6, 6, 2]
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                self.cup.roll_all()

                if self.visualize_gui: self.writeInfo(f"[STARTING ROLL] Player {self.turn +1} rolls the dice and rolled {self.cup.dice}")
                if self.visualize_gui: self.drawDice(self.cup.dice)



                if self.players[self.turn].bid_strategy == 'truthful':
                    self.current_bid = copy(self.cup.dice)
                elif self.players[self.turn].bid_strategy == 'knowledge_based':
                    self.current_bid = copy(self.cup.dice)
                else:
                    self.current_bid = random_bid_return()  # random bid

                self.update_knowledge()

                if self.visualize_gui: self.writeInfo(f"[STARTING BID] Player {self.turn +1} bids: {self.current_bid}")
                if self.visualize_gui: self.writeCurrentBid(self.current_bid)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                self.update_turn()
                
                self.state = states['believe/call_bluff_phase']
                continue

            if self.state == states['poker_phase']:
                threshold = self.current_bid[0]
                to_roll = []
                if self.visualize_gui: self.clearKnowledge()
                if self.visualize_gui: self.writeInfo(
                    f'[POKER PHASE] Player {self.turn +1} has three rolls to try and equal or beat {self.current_bid}.')
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                self.cup.roll_all()
                if self.visualize_gui: self.writeInfo(f'[ROLL 1] Player {self.turn +1} rolls the dice and rolls:')
                if self.visualize_gui: self.drawDice(self.cup.dice)
                # if self.print_info: print_dice(self.cup.dice)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                to_roll = self.roll_poker(threshold)

                if self.visualize_gui: self.writeInfo(f'[ROLL 2]')
                for d in to_roll:
                    # if self.visualize_gui: self.writeInfo(f'Rolling dice {d}:')
                    rollprint = self.cup.roll_dice_with_value(self.cup.dice[d],self.visualize_gui)
                    if self.visualize_gui: self.writeInfo(rollprint)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                if self.visualize_gui: self.drawDice(self.cup.dice)
                # if self.print_info: print_dice(self.cup.dice)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                to_roll = self.roll_poker(threshold)

                if self.visualize_gui: self.writeInfo(f'[ROLL 3]')
                for d in to_roll:
                    # if self.visualize_gui: self.writeInfo(f'Rolling dice {d}:')
                    rollprint = self.cup.roll_dice_with_value(self.cup.dice[d], self.visualize_gui)
                    if self.visualize_gui: self.writeInfo(rollprint)
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                if self.visualize_gui: self.drawDice(self.cup.dice)
                # if self.print_info: print_dice(self.cup.dice)

                if is_poker(self.cup.dice) and self.cup.dice[0] > threshold:
                    self.penalise_poker(2)
                elif is_poker(self.cup.dice) and self.cup.dice[0] == threshold:
                    self.penalise_poker(1)
                else:
                    self.penalise_poker(0)

                # if self.visualize_gui: self.writeInfo('[SCORE] is now as follows:')
                # for i in range(self.n_players):  # check if a player has lost (i.e has the max penalty points)
                #     if self.visualize_gui: self.writeInfo(f'Player {i +1}: {self.players[i].penalty_points} points: ')
                #     if self.visualize_gui: print_string = [self.loser_name[j] for j in
                #                                         range(self.players[i].penalty_points)]
                #     if self.visualize_gui: self.writeInfo("".join(print_string))
                # if self.print_info: print()  # if self.print_info: print for new line

                for i in range(self.n_players):  # check if a player has lost (i.e has the max penalty points)
                    if self.players[i].penalty_points == self.max_penalty:
                        if self.visualize_gui: self.writeInfo(
                            f'Player {i +1} has {self.max_penalty} penalty points and has lost the game!')
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
                if self.visualize_gui: self.removeOpenDice()

                for i in range(self.n_players):
                    penalty = self.loser_name[:self.players[i].penalty_points]
                    if self.visualize_gui: self.writePenalty(i, penalty)
                # if self.visualize_gui: self.writeInfo('[SCORE] is now as follows:')
                # for i in range(self.n_players):  # check if a player has lost (i.e has the max penalty points)
                #     if self.visualize_gui: self.writeInfo(f'Player {i}: {self.players[i].penalty_points} points: ')
                #     if self.visualize_gui: print_string = [self.loser_name[j] for j in
                #                                         range(self.players[i].penalty_points)]
                #     if self.visualize_gui: self.writeInfo("".join(print_string))
                # if self.print_info: print()  # if self.print_info: print for new line

                for i in range(self.n_players):  # check if a player has lost (i.e has the max penalty points)
                    if self.players[i].penalty_points == self.max_penalty:
                        if self.visualize_gui: self.writeInfo(
                            f'Player {i +1} has {self.max_penalty} penalty points and has lost the game!')
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
                if self.visualize_gui: self.writeInfo(f'[TURN] of Player {self.turn +1}')
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                if self.determine_bluff(
                        self.players[self.turn].determine_bluff_strategy):  # if true, then agent believes it is a bluff
                    if self.visualize_gui: self.writeInfo(
                        f'Player {self.turn +1} does not believe Player {(self.turn + self.n_players - 1) % self.n_players +1} (i.e. {self.current_bid} is not under the cup)')
                    self.state = states['penalty_phase']
                else:
                    if self.visualize_gui: self.writeInfo(
                        f'Player {self.turn +1} believes Player {(self.turn + self.n_players - 1) % self.n_players +1} (i.e. that at least {self.current_bid} is  under the cup)')
                    self.players[self.turn].knowledge = self.cup.dice

                    if is_poker(self.current_bid):
                        if self.visualize_gui: self.removeOpenDice()
                        self.state = states['poker_phase']
                    else:
                        if self.visualize_gui: self.removeOpenDice()
                        self.state = states['roll_dice_phase']
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                continue

            if self.state == states['roll_dice_phase']:
                self.roll_dice(self.players[self.turn].roll_strategy)
                if self.visualize_gui: self.writeInfo(f'Player {self.turn +1} has rolled the dice and rolled {self.cup.dice}.')
                if self.visualize_gui: self.drawDice(self.cup.dice)
                # if self.print_info: print_dice(self.cup.dice)
                self.update_knowledge()
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                self.state = states['bidding_phase']
                continue

            if self.state == states['bidding_phase']:
                self.bidding(self.players[self.turn].bid_strategy)
                if self.visualize_gui: self.writeInfo(f'Player {self.turn +1} has bid: {self.current_bid}')
                if self.visualize_gui: self.update_knowledge()
                if self.press_to_continue:
                    input("Press [Enter] to continue...\n")
                self.update_turn()
                self.state = states['believe/call_bluff_phase']
                continue
        if self.visualize_gui: self.writeInfo('Game finished!')
