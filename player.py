import os
import random
from color import Color


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')



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

        self.ships = []

    def valid_point(self, coordinate):
        return 0 <= coordinate[0] < self.height and 0 <= coordinate[1] < self.width

    def print_board(self, board: list[list[str]], title: str, alphabet: str) -> None:
        board_len = 36
        board_name_len = len(title)
        print(f"{'#' * ((board_len - board_name_len) // 2)} {title} BOARD {'#' * (round((board_len - board_name_len) / 2))}")
        print(" " * 5 + f"{' ' * 3}".join(self.ALPHABET))
        for ind, line in enumerate(board):

            line = [f'{Color.GREEN}{l}{Color.OFF}' if l not in [self.default_delimeter, "M", "H"] else l for l in line]
            print(f"{str(ind + 1)} {' ' if ind < 9 else ''}|{'|'.join(line)}|")

        print("\n")

    def show_boards(self, initialising=False):
        if not initialising:
            self.print_board(self.target_board, "TARGET", self.ALPHABET)
        self.print_board(self.personal_board, "PERSONAL", self.ALPHABET)

    def collect_coordinate(self, initialisation=False):
        while True:
            coord = input(f"Enter a {'starting ' if initialisation else ''}coordinate {'to hit' if not initialisation else ''} [eg: A3 or C10]: ")
            if 1 < len(coord) <= 3:
                if coord[0].isalpha() and coord[1].isdigit():
                    number_coord = coord[1:]

                    if number_coord.isdigit():
                        number_coord = int(number_coord)
                        if 1 <= number_coord <= self.height:
                            a = coord[0].upper()
                            if a in self.ALPHABET:
                                alpha_index = self.ALPHABET.index(a)
                                coordinate = (number_coord - 1, alpha_index)

                                current_coordinate_value = self.personal_board[coordinate[0]][coordinate[1]]
                                target_current_coordinate_value = self.target_board[coordinate[0]][coordinate[1]]

                                if initialisation and current_coordinate_value != self.default_delimeter:
                                    print(f"{Color.RED}This Position Clashes with another ship, Please try another coordinate{Color.OFF}")
                                    continue

                                if not initialisation and ("H" in target_current_coordinate_value or "M" in target_current_coordinate_value):
                                    print(f"{Color.RED}You have already hit this position, try again{Color.OFF}")
                                    continue

                                return coordinate

            # not valid coordinate
            clear()
            self.show_boards()
            print(f"{Color.RED}This Position is not valid, Please try another coordinate{Color.OFF}")

    def find_possible_orientations(self, start: tuple[int, int], length: int) -> list[tuple[str, tuple[int, int]]]:
        row, col = start
        possible = []
        for direction, (dr, dc) in ORIENTATIONS.items():
            coords = [(row + (dr * i), col + (dc * i)) for i in range(length + 1)]  # Get all the coordinates it would place
            if all(self.valid_point((r, c)) for r, c in coords):  # Check if ALL of the coordinates are in the grid
                if all(self.personal_board[r][c] == self.default_delimeter for r, c in coords):  # Check if all the coordinates are empty
                    possible.append((direction, (dr, dc)))

        return possible

    def collect_ship_coordinates(self):
        for ship, length in SHIPS.items():
            self.show_boards(initialising=True)

            ident = f' {ship[0].upper()} '
            print(f"Please enter the following details for the {Color.MAGENTA}{ship.title()}{Color.OFF} ship (length: {Color.MAGENTA}{length}{Color.OFF})")
            coordinates = self.collect_coordinate(initialisation=True)

            length -= 1

            possible_orientations = [a for a, b in self.find_possible_orientations(coordinates, length)]
            orientation = ""
            while orientation not in possible_orientations:
                orientation = input(f"Orientation {Color.GREEN}[{'/'.join(possible_orientations)}]{Color.OFF}: ").upper()
                if orientation not in possible_orientations:
                    clear()
                    print(f"{Color.RED}INCORRECT VALUE: TRY AGAIN AND USE THE OPTIONS SHOWN{Color.OFF}")

            # Add the boat to the graph
            orientation_direction = ORIENTATIONS[orientation]

            ship_buffer = []
            for x in range(length + 1):
                r, c = coordinates[0] + orientation_direction[0] * x, coordinates[1] + (orientation_direction[1] * x)
                self.personal_board[r][c] = ident
                ship_buffer.append((r, c))

            self.ships.append(ship_buffer)

            clear()

    def cpu_load_ship_locations(self):
        for ship, ship_length in SHIPS.items():
            # Pick a random coordinate
            row, column = 0, 0

            while True:
                row, column = random.randint(0, self.height - 1), random.randint(0, self.width - 1)

                if self.personal_board[row][column] != self.default_delimeter:  # It is not a valid point
                    continue  # Try again

                possible_orientations = [b for a, b in self.find_possible_orientations((row, column), ship_length - 1)]
                if len(possible_orientations) == 0:   # It clashes with another ship
                    continue

                orientation = random.randint(0, len(possible_orientations) - 1)
                orientation_direction = possible_orientations[orientation]

                ship_buffer = []
                for x in range(ship_length):
                    r, c = row + (orientation_direction[0] * x), column + (orientation_direction[1] * x)
                    self.personal_board[r][c] = f" {ship[0].upper()} "
                    ship_buffer.append((r, c))

                self.ships.append(ship_buffer)

                break

    def receive_hit(self, coordinate):
        """
        :param coordinate: where they want to hit at.
        :return: True (Hit) or False (Miss)
        """

        if self.personal_board[coordinate[0]][coordinate[1]] != self.default_delimeter:
            # Confirmed got hit
            self.health -= 1
            self.personal_board[coordinate[0]][coordinate[1]] = f"{Color.RED} H {Color.OFF}"

            for si, ship in enumerate(self.ships):
                if coordinate in ship:
                    print(f"SHIPS BEFORE: {self.ships}")

                    ship.remove(coordinate)
                    print(f"SHIPS NOW: {self.ships}")
                    if len(ship) == 0:
                        # SINK
                        self.ships.pop(si)
                        return "SINK"

                    break

            return True

        self.personal_board[coordinate[0]][coordinate[1]] = f"{Color.BLUE} M {Color.OFF}"

        return False

