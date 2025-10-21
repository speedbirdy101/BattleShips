from player import Player
from colorist import Color


def play_game():
    cpu = Player()
    user = Player()

    print(f"{Color.CYAN}Welcome to Battle Ships!{Color.OFF}")
    print("You will be playing a match against the computer, firstly, please enter the coordinates of 5 ships.\n")

    #  user.collect_ship_coordinates()  # Set up the board
    #  user.show_boards()

    cpu.cpu_load_ship_locations()
    cpu.show_boards(initialising=True)

    """
    All init processes complete.
    Now ready to start the main game
    """


if __name__ == '__main__':
    play_game()
