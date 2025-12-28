import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import re
    import math

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
    return math, np, os, re, sample


@app.cell
def _(os, re, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        data = data.strip().split("\n\n")
        # Store in dict: k=tile_id, value is numpy array with #=1, .=0
        tiles = {}
        for d in data:
            lines = d.split("\n")
            tile_id = int(re.findall(r"Tile (\d+):", lines[0])[0])
            tiles[tile_id] = [
                [int(i) for i in list(l.replace("#", "1").replace(".", "0"))]
                for l in lines[1:]
            ]
        print(tiles)
        return tiles


    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (
            f"input_{day_number}_sample{'_' + str(sample) if int(sample) > 1 else ''}.txt"
            if sample
            else f"input_{day_number}.txt"
        )
        return post_process(open(filename, "r").read())


    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data, math, np):
    def bin2num(b):
        """Convert list of 1 and 0 to a single int"""
        return int(sum([n * 2**i for i, n in enumerate(b[::-1])]))


    def extract_sides_bin(tile: np.ndarray):
        """Return 1 int per side in a list: [top, right, bottom, left], and the same flipped"""
        tile_transposed = np.transpose(tile)
        return [
            bin2num(tile[0]),
            bin2num(tile_transposed[-1]),
            bin2num(tile[-1]),
            bin2num(tile_transposed[0]),
            bin2num(tile[0][::-1]),
            bin2num(tile_transposed[-1][::-1]),
            bin2num(tile[-1][::-1]),
            bin2num(tile_transposed[0][::-1]),
        ]


    def invert_dict(d):
        """Turn format {a: [1,2], b: [2,3]} in {1: [a], 2: [a, b], 3: [b]}"""
        pairs = [(value, key) for key, values in d.items() for value in values]
        return {k: [v for k2, v in pairs if k2 == k] for k, _ in pairs}


    def generate_edges(data):
        """Generate lookup table of all edges per tile id and all tiles per edge (for easy lookup)"""
        edges = {k: extract_sides_bin(data[k]) for k in data.keys()}
        edge_lookup = invert_dict(edges)
        return edges, edge_lookup


    def problem_a(data):
        """Quick way to find corners only. Note that the solution in problem b can also solve problem a."""
        edges, edge_lookup = generate_edges(data)
        edge_counts = {}
        # Count total number each edge for a tile appears for all tiles
        for k in edges.keys():
            edge_counts[k] = [sum([len(edge_lookup[e]) for e in edges[k]])]
        # Count 12 is corner (2 common edges), 14 is side (3 common edges) and 16 is middle (4 common edges)
        print(
            "Tiles per overlapping edge count:",
            {k: len(v) for k, v in invert_dict(edge_counts).items()},
        )
        return math.prod(invert_dict(edge_counts)[12])


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data, np):
    def image_variants(img):
        """Compute all 8 rotations of an image. (4 normal rotations, 4 transposed rotations)"""
        img = np.array(img)
        img_T = np.transpose(img)
        return [
            img,
            np.rot90(img),
            np.rot90(np.rot90(img)),
            np.rot90(np.rot90(np.rot90(img))),
            img_T,
            np.rot90(img_T),
            np.rot90(np.rot90(img_T)),
            np.rot90(np.rot90(np.rot90(img_T))),
        ]


    def get_key_grid(img_map):
        """Return a matrix with the keys in there, to check against the example in the exercise.
        Keep in mind that coordinates are [x, y], but matrix is [-y, x] (note the -).
        Also note that the result of problem a can be obtained with:
        key_grid[0, 0] * key_grid[0, -1] * key_grid[-1, 0] * key_grid[-1, -1]"""
        coordinates = [v[0] for v in img_map.values()]
        min_x, max_x = (
            min([c[0] for c in coordinates]),
            max([c[0] for c in coordinates]),
        )
        min_y, max_y = (
            min([c[1] for c in coordinates]),
            max([c[1] for c in coordinates]),
        )
        grid = np.zeros((max_y - min_y + 1, max_x - min_x + 1))
        for k, v in img_map.items():
            xi, yi = v[0]
            grid[(grid.shape[0] - (yi - min_y) - 1, xi - min_x)] = k
        return grid


    def create_image_map(data):
        """Function to create full image map. This can be used to calculate problems a and b"""
        # Store all rotations of each image
        all_variants = {id: image_variants(data[id]) for id in data.keys()}

        # Keep track of keys
        k_cur = next(iter(all_variants.keys()))
        next_keys = set()

        # img_map is the resulting grid of images
        img_map = {k_cur: ((0, 0), all_variants[k_cur][0])}

        # Keep looping until there is no new k_cur to be found
        while k_cur is not None:
            # Extract sides/edges of img k_cur
            edge_left = img_map[k_cur][1][:, 0]
            edge_right = img_map[k_cur][1][:, -1]
            edge_up = img_map[k_cur][1][0, :]
            edge_down = img_map[k_cur][1][-1, :]

            # Store coordinates of k_cur for ease of access
            x, y = img_map[k_cur][0]

            for k in all_variants.keys():
                # If k is already in the image map, continue
                if k in img_map.keys():
                    continue
                # Check all possible images
                for img in all_variants[k]:
                    # Check left against right of k
                    if np.array_equal(edge_left, img[:, -1]):
                        next_keys.add(k)
                        img_map[k] = ((x - 1, y), img)
                        break
                    # Check right against left of k
                    if np.array_equal(edge_right, img[:, 0]):
                        next_keys.add(k)
                        img_map[k] = ((x + 1, y), img)
                        break

                    # Check up against down of k
                    if np.array_equal(edge_up, img[-1, :]):
                        next_keys.add(k)
                        img_map[k] = ((x, y + 1), img)
                        break

                    # Check down against up of k
                    if np.array_equal(edge_down, img[0, :]):
                        next_keys.add(k)
                        img_map[k] = ((x, y - 1), img)
                        break

            # Pick next current key until no more left
            if len(next_keys):
                k_cur = next_keys.pop()
            else:
                k_cur = None
        return img_map


    def print_grid(g):
        """Print visual grid with # and ."""
        for i in range(g.shape[0]):
            for j in range(g.shape[1]):
                print("#" if g[i, j] else ".", end="")
            print()
        print()


    def compose_full_image(img_map):
        """Remove borders of the snippets and compose the full image to find sea monsters."""
        # Crop the edge of the images for each ID
        img_snippets = {k: img_map[k][1][1:-1, 1:-1] for k in img_map.keys()}
        # Compose a list of lists with the img snippets in there
        key_grid = get_key_grid(img_map)
        img_grid = []
        for i in range(key_grid.shape[0]):
            line = []
            for j in range(key_grid.shape[1]):
                line.append(img_snippets[key_grid[i, j]])
            img_grid.append(line)
        # Return np.block, which stitches np arrays togeher
        return np.block(img_grid)


    def monster_patterns():
        """Monster pattern is given in the exercise. Convert to np array with ones and zeros.
        Then, rotate and transpose to get all variants, and return a list of coordinates where values are 1."""
        # Convert input from exercise to 2d numpy array of ones and zeros
        inp = "                  # \n#    ##    ##    ###\n #  #  #  #  #  #   "
        pattern = [
            [int(i) for i in list(l.replace("#", "1").replace(" ", "0"))]
            for l in inp.split("\n")
        ]

        # Get all variants of monsters
        pattern_variants = image_variants(pattern)
        return pattern_variants


    def problem_b(data):
        """Recalculated entire grid, since the method used in problem a is not sufficient for problem b."""
        img_map = create_image_map(data)
        key_grid = get_key_grid(img_map)
        img = compose_full_image(img_map)
        print(key_grid)

        # Scan each monster pattern, and check if an image is valid
        patterns = monster_patterns()
        for p in patterns:
            # Convert matrix of 1 and 0 to coordinates of the ones.
            coords_to_zero = np.argwhere(p)
            # Scan through the image to make sure the pattern is tested everywhere
            for i in range(img.shape[0] - p.shape[0]):
                for j in range(img.shape[1] - p.shape[1]):
                    # Check if the entire pattern is there
                    pattern_found = True
                    for c in coords_to_zero:
                        if img[i + c[0], j + c[1]] == 0:
                            pattern_found = False
                    # If the entire pattern is there, loop again to reset the values to 0
                    if pattern_found:
                        for c in coords_to_zero:
                            img[i + c[0], j + c[1]] = 0
        return np.sum(img)


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
