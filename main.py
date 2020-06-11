from game import Game, AllPossibleWorlds
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
    new_game = False
    test_string = ['S', 'M', 'E', 'G', 'M', 'A']
    public_knowledge = [6, 4]
    # a = public_knowledge[0]
    # print(a)
    # print([s for s in AllPossibleWorlds if public_knowledge in s])
    # print(AllPossibleWorlds[j] for j in AllPossibleWorlds if 6 in AllPossibleWorlds)
    pk1, pk2 = public_knowledge

    '''
    below are the 4 cases that can happen when one player has throw the dice, and the next player decides to keep one or two dice hidden under the cup
    while throwing the others open (in terms of possible worlds for the first player). This can be used for when we implement that type of knowledge later   '''
    # example when 1 die is open (5) and 2 known are under the cup, drawn from (6,4,4)
    worlds = [s for s in AllPossibleWorlds if 5 in s and ((6 in s and 4 in s) or s.count(4) >= 2)]
    # example when 1 die is open (2) and 2 known are under the cup, drawn from (6,5,4)
    worlds = [s for s in AllPossibleWorlds if
              2 in s and ((6 in s and 4 in s) or (6 in s and 5 in s) or (4 in s and 5 in s))]
    # example when 2 dice are open and one known is under the cup, drawn from (6,5,4)
    worlds = [s for s in AllPossibleWorlds if 1 in s and 5 in s and (6 in s or 5 in s or 4 in s)]
    # example when 2 dice are open and one known is under the cup, drawn from (6,4,4)
    worlds = [s for s in AllPossibleWorlds if 1 in s and 5 in s and (6 in s or 4 in s)]

    print(f'# worlds : {len(worlds)}: {worlds}')
    # print([s for s in AllPossibleWorlds if public_knowledge in s])
    # print(list(s for s in AllPossibleWorlds if s.count(pk1) >= 2))
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
