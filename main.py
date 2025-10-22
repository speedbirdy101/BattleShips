from player import Player, clear, ORIENTATIONS
from color import Color
import random


def hit_coordinate(coordinate, hitter, receiver):
    hit = receiver.receive_hit(coordinate)

    hitter.target_board[coordinate[0]][
        coordinate[1]] = f"{Color.RED} H {Color.OFF}" if hit else f"{Color.BLUE} M {Color.OFF}"

    return hit


def user_turn(user, cpu):
    coordinate = user.collect_coordinate()
    result = hit_coordinate(coordinate, user, cpu)

    msg = ""
    if result == "SINK":
        msg = f"{Color.RED}You sunk a ship!{Color.OFF}"
    elif result:
        msg = f"{Color.GREEN}You hit a ship!{Color.OFF}"
    else:
        msg = f"{Color.BLUE}You missed!{Color.OFF}"

    return msg


cpu_queue = []


def remove_first_queue():
    cpu_queue[0][1].pop(0)
    if len(cpu_queue[0][1]) == 0:  # If the instruction has no other directions we delete the whole thing
        cpu_queue.pop(0)


def cpu_turn(user, cpu):
    """
    CPU Mind:
    Queue: []

    1. Randomly pick coordinates
    2. Keep picking until a hit is found.
    3. Try all coordinates around it until we find a second hit
    4. Carry on in that direction
        -> if there is nothing else in that direction after having found the second hit & NO SINK REPORTED,
         we add it to the queue, as it must be another ship.

    5. Keep searching around the coordinate
    6. Repeat for any others in the queue
    7. Keep hitting randomly until we can repeat
    """
    next_coordinate = (0, 0)
    output_description = ""

    if len(cpu_queue) == 0:
        # Make a random choice as we have no leads
        while True:
            next_coordinate = random.randint(0, user.height - 1), random.randint(0, user.width - 1)
            if cpu.target_board[next_coordinate[0]][next_coordinate[1]] != cpu.default_delimeter:
                continue

            break

        hit = hit_coordinate(next_coordinate, cpu, user)

        if hit == "SINK":
            output_description = f"{Color.RED}The Computer sunk one of your ships!{Color.OFF}"

        elif hit:
            possible_orientations = []
            for a, b in ORIENTATIONS.items():
                if cpu.valid_point((next_coordinate[0] + b[0], next_coordinate[1] + b[1])):
                    v = cpu.target_board[
                        next_coordinate[0] + b[0]
                    ][
                        next_coordinate[1] + b[1]
                    ]

                    if "H" not in v and "M" not in v:
                        possible_orientations.append(b)

            cpu_queue.append(
                (next_coordinate, possible_orientations)
            )

            output_description = f"{Color.RED}The Computer hit one of your ships!{Color.OFF}"

        else:
            output_description = f"{Color.GREEN}The Computer missed!{Color.OFF}"

    else:
        # Unpacking
        next_queue_element = cpu_queue[0]
        base_coordinate = next_queue_element[0]
        next_direction = next_queue_element[1]

        # If the next instruction is empty, we remove it and try everything again
        if len(next_direction) == 0:
            cpu_queue.pop(0)
            return cpu_turn(user, cpu)

        # Find the next coordinate to hit
        next_direction = next_direction[0]

        next_coordinate = (
            base_coordinate[0] + next_direction[0],
            base_coordinate[1] + next_direction[1]
        )

        if not cpu.valid_point(next_coordinate):
            remove_first_queue()
            return cpu_turn(user, cpu)

        hit = hit_coordinate(next_coordinate, cpu, user)

        # Get rid of that direction now that we have hit it
        remove_first_queue()

        if hit and hit != "SINK":  # If we get a sink, we do not need to continue in that direction
            directions_to_try = [next_direction]
            for a, b in ORIENTATIONS.items():
                if b != next_direction and b != (-next_direction[0], -next_direction[1]):
                    directions_to_try.append(b)

            cpu_queue.insert(0, (next_coordinate, directions_to_try))  # Add the next point to try if we hit, but no sink
            """
            DONE:
                we will add next_direction first (as already done above)
                Then we will add the 2 other directions (not the one we came from -[next_direction] and not the one we are going to)
            """

            output_description = f"{Color.RED}The Computer hit one of your ships!{Color.OFF}"

        elif hit == "SINK":
            output_description = f"{Color.RED}The Computer sunk one of your ships!{Color.OFF}"

        else:
            output_description = f"{Color.GREEN}The Computer missed!{Color.OFF}"

    readable_coordinates = f'{cpu.ALPHABET[next_coordinate[1]]}{next_coordinate[0] + 1}'

    return readable_coordinates, output_description


def play_again():
    play_gain = input("\n\nWould you like to play again? [y/n]")

    if play_gain.lower() not in ["y", "n"]:
        clear()
        print(f"{Color.RED}Not a valid input, please try again{Color.OFF}")
        play_again()

    if play_gain.lower() == "y":
        clear()
        play_game()

    else:
        clear()
        print("Ok Bye!")
        return


def play_game():
    cpu = Player()
    user = Player()

    print(f"{Color.CYAN}Welcome to Battle Ships!{Color.OFF}")
    print("You will be playing a match against the computer, firstly, please enter the coordinates of 5 ships.\n")

    user.collect_ship_coordinates()  # Set up the board
    cpu.cpu_load_ship_locations()

    """
    All init processes complete.
    Now ready to start the main game
    """

    clear()

    count = 1
    cpu_choice = ""
    cpu_choice_output_buffer = ""
    user_choice_output_buffer = ""
    while user.health > 0 and cpu.health > 0:
        user.show_boards()
        print(
            f"{Color.CYAN}The game is now ready to be played, both players have picked the locations of their ships!{Color.OFF}")
        print(f"The {Color.MAGENTA}Target Board{Color.OFF} is where you are hitting, use it to record where you have hit before, and recognise where a ship could be located.")
        print(f"The {Color.MAGENTA}Personal Board{Color.OFF} is where your ships are located, you will be able to see where the CPU hits on this board.\n")
        # cpu.show_boards(initialising=True)

        if count % 2 == 0:  # Even: CPU
            cpu_choice, cpu_choice_output_buffer = cpu_turn(user, cpu)
            cpu_choice = f"The Computer chose {Color.MAGENTA}{cpu_choice}{Color.OFF}"

        else:  # Odd: User
            print(f"The Computer has sunk {Color.YELLOW}{5 - len(user.ships)}{Color.OFF} ships, you have sunk {Color.YELLOW}{5 - len(cpu.ships)}{Color.OFF} ships.\n")

            if cpu_choice != "" and cpu_choice_output_buffer != "":
                print(f"{cpu_choice} - {cpu_choice_output_buffer}")

            if user_choice_output_buffer != "":
                print(user_choice_output_buffer)

            user_choice_output_buffer = user_turn(user, cpu)

        clear()

        count += 1

    if user.health == 0:
        print(f"{Color.RED}You Lost! You needed another {cpu.health} hits{Color.OFF}")

    elif cpu.health == 0:
        print(f"{Color.GREEN}You Won! The computer needed {user.health} more hits{Color.OFF}")

    # Option to play again
    play_again()


if __name__ == '__main__':
    play_game()


"""

Notes:
- I have added the ability for the CPU to intelligently target ships once it has found a hit, to target ships close together.
  However in doing this, it is making it worse in a way, as the CPU is now trying every single possible direction around a EVERY hit, which is not optimal.
  This is optimal in some cases, but not all, as it can lead to wasted hits in lots of scenarios.
  
To consider:
- I am not too sure if when the CPU hits, and it reports a H, it is correct.
  It seemed that the CPU hit points around the area it found a confirmed hit, but a lot of the points which i THINK should have been misses were reported as hits.
  I may be making this up --> need to test more thoroughly (Remove clear ability to be able to look back into the past. & log CPU personal board.)


"""