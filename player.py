import os

clear = lambda: os.system('cls')

ALPHABET = "ABCDEFGHIJ"
ships = {
    "carrier": 5,
    "battleship": 4,
    "destroyer": 3,
    "submarine": 3,
    "patrol": 2
}

class Player:
    def __init__(self):
        self.health = 17
        self.personal_board = [
            [" - " for i in range(10)] for j in range(10)
        ]

        self.target_board = [
            [" - " for i in range(10)] for j in range(10)
        ]

    def show_boards(self):
        for board, board_name in [(self.personal_board, "PERSONAL"), (self.target_board, "TARGET")]:
            board_len = 36
            board_name_len = len(board_name)
            print(f"{'#' * ((board_len - board_name_len) // 2)} {board_name} BOARD {'#' * (round((board_len - board_name_len) / 2))}")
            print(" " * 5 + "   ".join(ALPHABET))
            for ind, line in enumerate(board):
                print(f"{str(ind + 1)} {" " if ind < 9 else ""}|{"|".join(line)}|")

            print("\n\n")

    def collect_coordinate(self, starting=False):
        while True:
            coord = input(f"Enter a {'starting ' if starting else ''}coordinate [eg: A3 or C10]: ")
            if coord[0].isalpha() and coord[1].isdigit():
                number_coord = coord[1:]

                if number_coord.isdigit():
                    number_coord = int(number_coord)
                    if 0 <= number_coord <= 10:
                        coordinate = (ALPHABET.index(coord[0].upper()), number_coord)
                        return coordinate

            else:  # not valid coordinate
                clear()
                print("NOT A VALID COORDINATE, PLEASE TRY AGAIN")

        return None

    def collect_ship_coordinates(self):
        coordinates = self.collect_coordinate(starting=True)
        print(f"\n\nChosen coordinate: {coordinates}")
        clear()

        possible_orientations = ["L", "R", "U", "D"]
        for ship, length in ships.items():
            print(f"Please enter the following details for the {ship} ship (length: {length})")
            orientation = ""
            while orientation not in possible_orientations:
                orientation = input(f"Orientation [{'/'.join(possible_orientations)}]: ").upper()
                if orientation not in possible_orientations:
                    clear()
                    print("INCORRECT VALUE: TRY AGAIN AND USE THE OPTIONS SHOWN")
                    continue
