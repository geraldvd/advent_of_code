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
    return np, os, sample


@app.cell
def _(np, os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        data = np.array(
            [
                [
                    int(i)
                    for i in list(d.strip().replace("#", "1").replace(".", "0"))
                ]
                for d in data
            ]
        )
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
def _(input_data, np):
    def calculate_neighbours(coord):
        x, y, z = coord
        neighbours = []
        for xi in [-1, 0, +1]:
            for yi in [-1, 0, +1]:
                for zi in set([-1, 0, +1]):
                    if xi == yi == zi == 0:
                        continue
                    neighbours.append((x + xi, y + yi, z + zi))
        return neighbours


    def coord_minmax(coords, axis):
        """Find min and max coordinates in a list of coordinates for single axis, and go 1 below and above"""
        coord_list = [c[axis] for c in coords]
        return min(coord_list) - 1, max(coord_list) + 1


    def problem_a(data):
        active_cubes = set([(int(c[0]), int(c[1]), 0) for c in np.argwhere(data)])
        for i in range(6):
            x_min, x_max = coord_minmax(active_cubes, 0)
            y_min, y_max = coord_minmax(active_cubes, 1)
            z_min, z_max = coord_minmax(active_cubes, 2)
            new_active_cubes = set()
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    for z in range(z_min, z_max + 1):
                        coord = (x, y, z)
                        neighbours = calculate_neighbours(coord)
                        # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
                        # Otherwise, the cube becomes inactive.
                        if coord in active_cubes:
                            if sum(
                                [1 for n in neighbours if n in active_cubes]
                            ) in [2, 3]:
                                new_active_cubes.add(coord)

                        # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
                        # Otherwise, the cube remains inactive.
                        else:
                            if (
                                sum([1 for n in neighbours if n in active_cubes])
                                == 3
                            ):
                                new_active_cubes.add(coord)
            active_cubes = new_active_cubes.copy()
        return len(active_cubes)


    answer_a = problem_a(input_data)
    return answer_a, coord_minmax


@app.cell
def _(coord_minmax, input_data, np):
    def calculate_neighbours_4d(coord):
        x, y, z, w = coord
        neighbours = []
        for xi in [-1, 0, +1]:
            for yi in [-1, 0, +1]:
                for zi in set([-1, 0, +1]):
                    for wi in set([-1, 0, +1]):
                        if xi == yi == zi == wi == 0:
                            continue
                        neighbours.append((x + xi, y + yi, z + zi, w + wi))
        return neighbours


    def problem_b(data):
        active_cubes = set(
            [(int(c[0]), int(c[1]), 0, 0) for c in np.argwhere(data)]
        )
        for i in range(6):
            x_min, x_max = coord_minmax(active_cubes, 0)
            y_min, y_max = coord_minmax(active_cubes, 1)
            z_min, z_max = coord_minmax(active_cubes, 2)
            w_min, w_max = coord_minmax(active_cubes, 3)
            new_active_cubes = set()
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    for z in range(z_min, z_max + 1):
                        for w in range(w_min, w_max + 1):
                            coord = (x, y, z, w)
                            neighbours = calculate_neighbours_4d(coord)
                            # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
                            # Otherwise, the cube becomes inactive.
                            if coord in active_cubes:
                                if sum(
                                    [1 for n in neighbours if n in active_cubes]
                                ) in [2, 3]:
                                    new_active_cubes.add(coord)

                            # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
                            # Otherwise, the cube remains inactive.
                            else:
                                if (
                                    sum(
                                        [
                                            1
                                            for n in neighbours
                                            if n in active_cubes
                                        ]
                                    )
                                    == 3
                                ):
                                    new_active_cubes.add(coord)
            active_cubes = new_active_cubes.copy()
        return len(active_cubes)


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
