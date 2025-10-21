import os
import random
from colorist import Color


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    pass


SHIPS = {
    "carrier": 5,
    "battleship": 4,
    "destroyer": 3,
    "submarine": 3,
    "patrol": 2
}
ORIENTATIONS = {
    "L": (0, -1),
    "R": (0, 1),
    "D": (1, 0),
    "U": (-1, 0)
}


class Player:
    def __init__(self):
        self.health = 17

        self.height = 10
        self.width = 10
        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.width]
        self.default_delimeter = " - "

        self.personal_board = [
            [self.default_delimeter for i in range(self.width)] for j in range(self.height)
        ]

        self.target_board = [
            [self.default_delimeter for i in range(self.width)] for j in range(self.height)
        ]

    def print_board(self, board: list[list[str]], title: str, alphabet: str) -> None:
        board_len = 36
        board_name_len = len(title)
        print(f"{'#' * ((board_len - board_name_len) // 2)} {title} BOARD {'#' * (round((board_len - board_name_len) / 2))}")
        print(" " * 5 + f"{' ' * 3}".join(self.ALPHABET))
        for ind, line in enumerate(board):

            line = [f'{Color.BLUE}{l}{Color.OFF}' if l != self.default_delimeter else l for l in line]
            print(f"{str(ind + 1)} {' ' if ind < 9 else ''}|{'|'.join(line)}|")

        print("\n\n")

    def show_boards(self, initialising=False):
        if not initialising:
            self.print_board(self.target_board, "TARGET", self.ALPHABET)
        self.print_board(self.personal_board, "PERSONAL", self.ALPHABET)

    def collect_coordinate(self, initialisation=False):
        while True:
            coord = input(f"Enter a {'starting ' if initialisation else ''}coordinate [eg: A3 or C10]: ")
            if coord[0].isalpha() and coord[1].isdigit():
                number_coord = coord[1:]

                if number_coord.isdigit():
                    number_coord = int(number_coord)
                    if 1 <= number_coord <= self.height:
                        try:
                            alpha_index = self.ALPHABET.index(coord[0].upper())
                            coordinate = (number_coord - 1, alpha_index)

                            if initialisation and self.personal_board[coordinate[0]][coordinate[1]] == self.default_delimeter:
                                return coordinate

                            else:
                                print(f"{Color.RED}This Position Clashes with another ship, Please try another coordinate{Color.OFF}")
                                continue

                        except ValueError as error:
                            pass  # It is not in the alphabet

            # not valid coordinate
            clear()
            print(f"{Color.RED}This Position is not valid, Please try another coordinate{Color.OFF}")

    def find_possible_orientations(self, start: tuple[int, int], length: int) -> list[str]:
        row, col = start
        possible = []
        for direction, (dr, dc) in ORIENTATIONS.items():
            coords = [(row + dr * i, col + dc * i) for i in range(length + 1)]
            if all(0 <= r < self.height and 0 <= c < self.width for r, c in coords):
                if all(self.personal_board[r][c] == self.default_delimeter for r, c in coords):
                    possible.append(direction)
        return possible

    def collect_ship_coordinates(self):
        for ship, length in SHIPS.items():
            self.show_boards(initialising=True)

            ident = f' {ship[0].upper()} '
            print(f"Please enter the following details for the {Color.MAGENTA}{ship.title()}{Color.OFF} ship (length: {Color.MAGENTA}{length}{Color.OFF})")
            coordinates = self.collect_coordinate(initialisation=True)

            length -= 1

            possible_orientations = self.find_possible_orientations(coordinates, length)
            orientation = ""
            while orientation not in possible_orientations:
                orientation = input(f"Orientation {Color.GREEN}[{'/'.join(possible_orientations)}]{Color.OFF}: ").upper()
                if orientation not in possible_orientations:
                    clear()
                    print("INCORRECT VALUE: TRY AGAIN AND USE THE OPTIONS SHOWN")

            # Add the boat to the graph
            orientation_direction = ORIENTATIONS[orientation]

            for x in range(length + 1):
                r, c = coordinates[0] + orientation_direction[0] * x, coordinates[1] + (orientation_direction[1] * x)
                self.personal_board[r][c] = ident

            clear()

    def cpu_load_ship_locations(self):
        for ship, ship_length in SHIPS.items():
            # Pick a random coordinate
            row, column = 0, 0

            while True:
                row, column = random.randint(0, self.height - 1), random.randint(0, self.width - 1)

                if self.personal_board[row][column] != self.default_delimeter:  # It is not a valid point
                    continue  # Try again

                possible_orientations = self.find_possible_orientations((row, column), ship_length - 1)
                if len(possible_orientations) == 0:   # It clashes with another ship
                    continue

                orientation = random.randint(0, len(possible_orientations) - 1)
                orientation = possible_orientations[orientation]
                orientation_direction = ORIENTATIONS[orientation]

                for x in range(ship_length):
                    r, c = row + (orientation_direction[0] * x), column + (orientation_direction[1] * x)
                    self.personal_board[r][c] = f" {ship[0].upper()} "

                break
