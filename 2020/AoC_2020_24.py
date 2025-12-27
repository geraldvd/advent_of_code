import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
    return os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        data = [d.strip() for d in data]
        print(data)
        return data


    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (
            f"input_{day_number}_sample{'_' + str(sample) if int(sample) > 1 else ''}.txt"
            if sample
            else f"input_{day_number}.txt"
        )
        return post_process(open(filename, "r").readlines())


    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data):
    def parse_direction_string(s):
        """convert string of directions without delimiter to delimited list"""
        directions = []
        i = 0
        while i < len(s):
            # If it starts with n or s, it means it's ne/nw/se/sw.
            if s[i] in ["n", "s"]:
                directions.append(s[i : i + 2])
                i += 2
            # Else it must be e or w
            else:
                directions.append(s[i])
                i += 1
        return directions


    def direction_to_coordinate(d):
        """Convert directions to coordinates (x, y). For a hexagon, the nett displacement stays the same.
        I.e., for E and W, it is 1 and for NE/NW/SE/SW it is 0.5. Doubled here to stick to integer values."""
        match d:
            case "e":
                return (2, 0)
            case "w":
                return (-2, 0)
            case "ne":
                return (1, 1)
            case "nw":
                return (-1, 1)
            case "se":
                return (1, -1)
            case "sw":
                return (-1, -1)
            case _:
                print("Error: this direction should not exist.")


    def calculate_tile_coordinate(directions):
        """Convert sequence of directions to coordinates of a tile"""
        c = (0, 0)
        for d in directions:
            move = direction_to_coordinate(d)
            c = (c[0] + move[0], c[1] + move[1])
        return c


    def calculate_black_tiles(data):
        """Create a set of all black tiles. Needed for both problem a and problem b."""
        black_tiles = set()
        for d in data:
            moves = parse_direction_string(d)
            tile = calculate_tile_coordinate(moves)
            if tile in black_tiles:
                black_tiles.remove(tile)
            else:
                black_tiles.add(tile)
        return black_tiles


    def problem_a(data):
        black_tiles = calculate_black_tiles(data)
        return len(black_tiles)


    answer_a = problem_a(input_data)
    return answer_a, calculate_black_tiles


@app.cell
def _(calculate_black_tiles, input_data):
    def get_neighbours(tile):
        """Compute 6 neighbours of a given tile (x, y)."""
        return [
            (tile[0] + 2, tile[1]),  # e
            (tile[0] - 2, tile[1]),  # w
            (tile[0] + 1, tile[1] + 1),  # ne
            (tile[0] - 1, tile[1] + 1),  # nw
            (tile[0] + 1, tile[1] - 1),  # se
            (tile[0] - 1, tile[1] - 1),  # sw
        ]


    def problem_b(data):
        # Starting point is where problem a left of
        black_tiles = calculate_black_tiles(data)
        for day in range(100):
            new_black_tiles = set()
            for bt in black_tiles:
                neighbours = get_neighbours(bt)
                # Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
                num_black_neighbours = sum(
                    [1 if n in black_tiles else 0 for n in neighbours]
                )
                if not (num_black_neighbours == 0 or num_black_neighbours > 2):
                    new_black_tiles.add(bt)

                # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
                # White tiles are not directly stored, so instead just look at all neighbours.
                # (Any tile outside that cannot apply to the conditions.)
                for n in neighbours:
                    # Consider tile n to be the one that needs to be checked, if it is white.
                    if n not in black_tiles:
                        # Get neighbours of this new white tile
                        neighbours_2 = get_neighbours(n)
                        num_black_neighbours = sum(
                            [1 if n2 in black_tiles else 0 for n2 in neighbours_2]
                        )
                        if num_black_neighbours == 2:
                            new_black_tiles.add(n)
            black_tiles = new_black_tiles.copy()
            print(f"Day {day + 1}: {len(black_tiles)}")
        return len(black_tiles)


    answer_b = problem_b(input_data)
    return (answer_b,)


@app.cell
def _(answer_a, answer_b, day_number):
    # Show answers
    print(f"Day {int(day_number)}a: {answer_a if answer_a else '-'}")
    print(f"Day {int(day_number)}b: {answer_b if answer_b else '-'}")
    return


if __name__ == "__main__":
    app.run()
