from game import Game, AllPossibleWorlds, losscount
from player import Player
from cup import Cup
import numpy as np
import time
from visualize_dice import Visualized_game



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


def main():
    new_game = True




    # meanchecks = np.arange(10/120, 60/120, 1/120) #tested performance for different mean believe thresholds
    # for mean in meanchecks:
    # print(f'Mean = {round(mean,3)}')

    ###############    Loop for testing many games, no prints or press to continue     ####################################
    # n_test_games = 1000
    # i = 0
    # t0 = time.time()
    # print(f'Playing {n_test_games} games for testing')
    # while i < n_test_games:
    #     game = Game(n_players=3, print_info = False, press_to_continue = False, visualise_game_gui=False)
    #     game.play()
    #     i += 1
    # print(f' Player 1 losses:{losscount[0]}, Player 2 losses:{losscount[1]}, Player 3 losses:{losscount[2]}')
    #
    # print(f'Computing time: {time.time()-t0}')


    ################    Loop for testing individual games, with info and press to continue     ####################################
    while new_game:  #
        game = Game()
        game.play()
        # i += 1
        another_game = input("Another game? [y/n]")
        while another_game != 'y' and another_game != 'n':
            another_game = input("Please try again: Another game? [y/n]")

        if another_game == 'n':
            new_game = False
            print('Goodbye!')

        if another_game == 'y':
            print('Starting new game!')
            continue


if __name__ == '__main__':
    main()






#
    # public_knowledge = [6, 4]
    # print(max(np.random.normal(3 / 12, 1 / 12, 1000) * 0.5))
    # print(max(np.random.normal(3 / 12, 1 / 12, 1000) * 0.75))
    # print(max(np.random.normal(3 / 12, 1 / 12, 1000)))
    # print(min(np.random.normal(3 / 12, 1 / 12, 1000)*0.5))
    # print(min(np.random.normal(3 / 12, 1 / 12, 1000) * 0.75))
    # print(min(np.random.normal(3 / 12, 1 / 12, 1000)))

    # a = public_knowledge[0]
    # print(a)
    # print([s for s in AllPossibleWorlds if public_knowledge in s])
    # print(AllPossibleWorlds[j] for j in AllPossibleWorlds if 6 in AllPossibleWorlds)
    # current_bid = [6, 4, 1]
    # higher_possible = [w for w in self.players[self.turn].knowledge if
    #                    AllPossibleWorlds.index(w) > AllPossibleWorlds.index(self.current_bid)]
    # print(len(higher_possible) / len(self.players[self.turn].knowledge))

    #
    # pk1, pk2 = public_knowledge

    '''
    below are the 4 cases that can happen when one player has throw the dice, and the next player decides to keep one or two dice hidden under the cup
    while throwing the others open (in terms of possible worlds for the first player). This can be used for when we implement that type of knowledge later   '''
    # # example when 1 die is open (5) and 2 known are under the cup, drawn from (6,4,4)
    # worlds = [s for s in AllPossibleWorlds if 5 in s and ((6 in s and 4 in s) or s.count(4) >= 2)]
    # # example when 1 die is open (2) and 2 known are under the cup, drawn from (6,5,4)
    # worlds = [s for s in AllPossibleWorlds if
    #           2 in s and ((6 in s and 4 in s) or (6 in s and 5 in s) or (4 in s and 5 in s))]
    # # example when 2 dice are open and one known is under the cup, drawn from (6,5,4)
    # worlds = [s for s in AllPossibleWorlds if 1 in s and 5 in s and (6 in s or 5 in s or 4 in s)]
    # # example when 2 dice are open and one known is under the cup, drawn from (6,4,4)
    # worlds = [s for s in AllPossibleWorlds if 1 in s and 5 in s and (6 in s or 4 in s)]

    # print(f'# worlds : {len(worlds)}: {worlds}')