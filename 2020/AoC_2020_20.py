import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import re
    import math

    # Settings
    sample = True # Fill in False, or the sample number (True and 1 are the same)
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
            tiles[tile_id] = [[int(i) for i in list(l.replace("#", "1").replace(".", "0"))] for l in lines[1:]]
        print(tiles)
        return tiles

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").read())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data, math, np):
    def bin2num(b):
        '''Convert list of 1 and 0 to a single int'''
        return int(sum([n*2**i for i, n in enumerate(b[::-1])]))

    def extract_sides_bin(tile : np.ndarray):
        '''Return 1 int per side in a list: [top, right, bottom, left], and the same flipped'''
        tile_transposed = np.transpose(tile)
        return [bin2num(tile[0]), bin2num(tile_transposed[-1]), bin2num(tile[-1]) , bin2num(tile_transposed[0]), \
               bin2num(tile[0][::-1]), bin2num(tile_transposed[-1][::-1]), bin2num(tile[-1][::-1]) , bin2num(tile_transposed[0][::-1])]

    def invert_dict(d):
        '''Turn format {a: [1,2], b: [2,3]} in {1: [a], 2: [a, b], 3: [b]}'''
        pairs = [(value, key) for key, values in d.items() for value in values]
        return {k: [v for k2, v in pairs if k2 == k] for k, _ in pairs}

    def generate_edges(data):
        '''Generate lookup table of all edges per tile id and all tiles per edge (for easy lookup)'''
        edges = {k:extract_sides_bin(data[k]) for k in data.keys()}
        edge_lookup = invert_dict(edges)
        return edges, edge_lookup

    def problem_a(data):
        edges, edge_lookup = generate_edges(data)
        edge_counts = {}
        # Count total number each edge for a tile appears for all tiles
        for k in edges.keys():
            edge_counts[k] = [sum([len(edge_lookup[e]) for e in edges[k]])]
        # Count 12 is corner (2 common edges), 14 is side (3 common edges) and 16 is middle (4 common edges)
        print("Tiles per overlapping edge count:", {k:len(v) for k, v in invert_dict(edge_counts).items()})
        return math.prod(invert_dict(edge_counts)[12])
    answer_a = problem_a(input_data)
    return answer_a, extract_sides_bin, generate_edges


@app.cell
def _(extract_sides_bin, generate_edges, input_data, np):
    def get_single_neighbour(tile, edge, edges, edge_lookup):
        neighbour = [e for e in edge_lookup[edge] if e != tile] if len(edge_lookup[edge])>1 else None
        print(neighbour)

    def get_neighbours2(k, tile, edges, edge_lookup):
        top, bottom, left, right = extract_sides_bin(tile)[:4]
        neighbour = [e for e in edge_lookup[top] if e != k][0] if len(edge_lookup[top])>1 else None
        print(top, bottom, left, right)
        print(neighbour)
        if neighbour:
            print(edges[neighbour])

    def get_neighbours(tile, edges, edge_lookup):
        neighbours = []
        for edge in edges[tile]:
            neighbour_found = [t for t in edge_lookup[edge] if t != tile]
            neighbours.append(neighbour_found[0] if len(neighbour_found) else None)
        return neighbours[:4]

    def get_tile_grid(tile_coords):
        min_x = min([c[0] for c in tile_coords.values()])
        max_x = max([c[0] for c in tile_coords.values()])
        min_y = min([c[1] for c in tile_coords.values()])
        max_y = max([c[1] for c in tile_coords.values()])
        grid = np.zeros((max_y-min_y, max_x-min_x))
        return grid

    def problem_b(data):
        edges, edge_lookup = generate_edges(data)
        key_list = list(data.keys())
        tile_coords = {k: None for k in key_list}
        tile_coords[key_list[0]] = (0, 0)
        counter = 0
        while None in tile_coords.values() and counter < 10:
            counter += 1
            for k in key_list:
                if not tile_coords[k]:
                    continue
                xi, yi = tile_coords[k]
                n_up, n_right, n_bottom, n_left = get_neighbours(k, edges, edge_lookup)
                if n_up: tile_coords[n_up] = (xi, yi+1)
                if n_right: tile_coords[n_right] = (xi+1, yi)
                if n_bottom: tile_coords[n_bottom] = (xi, yi-1)
                if n_left: tile_coords[n_left] = (xi-1, yi)
        print(tile_coords)
        print(get_tile_grid(tile_coords))
        # # Key is (x, y), value is (tile_id, bool(flipped))
        # tile_coords = {(0, 0): (start_key, False)}
        # adj_tiles = [(0, 0)]
        # while len(adj_tiles):
        #     new_adj_tiles = []
        #     for x, y in adj_tiles:
        #         t_id, t_flipped = tile_coords[(x, y)]
        #         for xi in [x-1, x+1]:
        #             for yi in [y-1, y+1]:

        #         for i, edge in enumerate(edges[t_id]):
        #             match i:
        #                 # UP
        #                 case 0:
        #                     neighbours = [t for t in edge_lookup[edge] if t != t_id]
        #                     assert len(neighbours) < 2, "Assumption that there is max 1 neighbour found"
        #                     if len(neighbours):
        #                         tile_coords[(xi, yi+1)] = (neighbours[0], False)
        #                         new_adj_tiles.append((xi, yi+1))


        #         print([edge_lookup[e] for e in edges[t_id]])
        #     break
        print()
        for k in edges.keys():
            print(k, edges[k])
            for e in edges[k]:
                get_single_neighbour(k, e, edges, edge_lookup)
        print()
        get_neighbours2(2311, data[2311], edges, edge_lookup)
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
    return


if __name__ == "__main__":
    app.run()
