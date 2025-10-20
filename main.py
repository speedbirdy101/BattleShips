import random
from player import Player


def play_game():
    cpu = Player()
    user = Player()

    user.show_boards()

    user.collect_ship_coordinates()


if __name__ == '__main__':
    play_game()
