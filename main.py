from game import Game, PossibleWorlds
from player import Player
from cup import Cup


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
    test_string = ['S', 'M', 'E', 'G', 'M', 'A']

    while new_game:
        game = Game()
        game.play()

        another_game = input("Another game? [y/n]")
        while another_game != 'y' and another_game != 'n':
            another_game = input("Please try again: Another game? [y/n]")

        if another_game == 'n':
            new_game = False
            print('Goodbye!')

        if another_game == 'y':
            print('Starting new game!')
            continue


    # print(game.p1.turn)
    # print(game.p2.turn)

    # print(game.cup.dice)
    # # print(len(PossibleWorlds))
    # print(PossibleWorlds.index(game.cup.dice))
    # print_dice(game.cup.dice)
    # game.cup.roll_dice_with_value(6)
    # print_dice(game.cup.dice)
    # game.cup.roll_all()
    # # print(game.cup.dice)
    # print(PossibleWorlds.index(game.cup.dice))

    # print(PossibleWorlds.index([5, 5, 5]))
    # print(PossibleWorlds.index([6, 6, 6]))

    # print(game.p1.knowledge)
    # print_dice(game.cup.dice)


if __name__ == '__main__':
    main()
