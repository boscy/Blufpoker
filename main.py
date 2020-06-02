from game import Game, PossibleWorlds
from player import Player
from cup import Cup


def main():
    game = Game()

    # print(game.p1.turn)
    # print(game.p2.turn)

    print(game.cup.dice)
    # print(len(PossibleWorlds))
    print(PossibleWorlds.index(game.cup.dice))

    # game.cup.roll_all()
    # print(game.cup.dice)
    # print(PossibleWorlds.index(game.cup.dice))

    # print(PossibleWorlds.index([5, 5, 5]))
    # print(PossibleWorlds.index([6, 6, 6]))

    game.cup.roll_dice_with_value(1)
    print(game.cup.dice)
    print(game.p1.knowledge)

if __name__ == '__main__':
    main()
