import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np

    # Settings
    sample = True  # Fill in False, or the sample number (True and 1 are the same)
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
        return (
            s.replace("se", "se,")
            .replace("sw", "sw,")
            .replace("nw", "nw,")
            .replace("ne", "ne,")
            .replace("ws", "w,s")
            .replace("wn", "w,n")
            .replace("es", "e,s")
            .replace("en", "e,n")
            .replace("ew", "e,w")
            .replace("we", "w,e")
            .replace("ee", "e,e")
            .replace("ww", "w,w")
            .replace("ee", "e,e")
            .replace("ww", "w,w")
            .strip(",")
            .split(",")
        )


    def norm_tile_tuple(tile):
        min_ns = min(tile[0], tile[2])
        min_ew = min(tile[1], tile[3])
        return (
            tile[0] - min_ns,
            tile[1] - min_ew,
            tile[2] - min_ns,
            tile[3] - min_ew,
        )


    def tile2tuple(tile):
        """Convert dict to (n, e, s, w)"""
        return norm_tile_tuple((tile["n"], tile["e"], tile["s"], tile["w"]))


    def netto_move(moves):
        dir_count = {"e": 0, "n": 0, "s": 0, "w": 0}
        for m in moves:
            for d in m:
                dir_count[d] += 2 // len(m)
        pairs = [("n", "s"), ("e", "w")]
        for p1, p2 in pairs:
            min_p1p2 = min(dir_count[p1], dir_count[p2])
            dir_count[p1] -= min_p1p2
            dir_count[p2] -= min_p1p2
        return dir_count


    def problem_a(data):
        tiles = {}
        for d in data:
            moves = parse_direction_string(d)
            nm = netto_move(moves)
            hash_nm = tile2tuple(nm)
            if hash_nm not in tiles.keys():
                tiles[hash_nm] = 0
            tiles[hash_nm] += 1
        print(tiles)
        return sum([i % 2 for i in tiles.values()])


    answer_a = problem_a(input_data)
    return (
        answer_a,
        netto_move,
        norm_tile_tuple,
        parse_direction_string,
        tile2tuple,
    )


@app.cell
def _(
    input_data,
    netto_move,
    norm_tile_tuple,
    parse_direction_string,
    tile2tuple,
):
    def get_neighbours(tile):
        """Return neighbour tiles: nw (n+1, w+1), ne (n+1, e+1), sw (s+1, w+1), se (s+1, e+1), e (e+2), w (w+2)"""
        return [
            norm_tile_tuple((tile[0] + 1, tile[1], tile[2], tile[3] + 1)),
            norm_tile_tuple((tile[0] + 1, tile[1] + 1, tile[2], tile[3])),
            norm_tile_tuple((tile[0], tile[1], tile[2] + 1, tile[3] + 1)),
            norm_tile_tuple((tile[0], tile[1] + 1, tile[2] + 1, tile[3])),
            norm_tile_tuple((tile[0], tile[1] + 2, tile[2], tile[3])),
            norm_tile_tuple((tile[0], tile[1], tile[2], tile[3] + 2)),
        ]


    def problem_b(data):
        # Short way to do problem a again (True is black, False is white)
        tiles = {}
        for d in data:
            tile = tile2tuple(netto_move(parse_direction_string(d)))
            tiles[tile] = True if tile not in tiles.keys() else not (tiles[tile])
        print(sum(tiles.values()))

        # Simulate 100 days
        for day in range(10):
            new_tiles = tiles.copy()
            for t in tiles.keys():
                # Get neighbours and count black ones. Also, add to tiles if not added yet.
                neighbours = get_neighbours(t)
                neighbours_black_count = 0
                for n in neighbours:
                    if n not in tiles.keys():
                        new_tiles[n] = False
                    if new_tiles[n]:
                        neighbours_black_count += 1
                # Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
                if tiles[t] and (
                    neighbours_black_count == 0 or neighbours_black_count > 2
                ):
                    new_tiles[t] = not (tiles[t])
                # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
                if not tiles[t] and neighbours_black_count == 2:
                    new_tiles[t] = not (tiles[t])
            tiles = new_tiles.copy()
            print(f"Day {day + 1}: {sum(tiles.values())}")

        return None


    answer_b = problem_b(input_data)
    return (answer_b,)


@app.cell
def _(answer_a, answer_b, day_number):
    # Show answers
    print(f"Day {int(day_number)}a: {answer_a if answer_a else '-'}")
    print(f"Day {int(day_number)}b: {answer_b if answer_b else '-'}")
    return


@app.cell
def _():
    a = [True, True, False, True]
    sum(a)
    return


@app.cell
def _():
    b = False if False else not (False)
    return (b,)


@app.cell
def _(b):
    b
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
