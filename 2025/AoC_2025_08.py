import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import math

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
    num_connections = 10 if sample else 1000
    return math, np, num_connections, os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        data = [tuple([int(i) for i in d.strip().split(",")]) for d in data]
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
    def distance(c1, c2):
        """Calculate euclidean distance"""
        x1, y1, z1 = c1
        x2, y2, z2 = c2
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


    def calculate_distances(data):
        # Calculate all distances in a matrix
        distances = np.ones((len(data), len(data)))
        for i1, c1 in enumerate(data):
            for i2, c2 in enumerate(data):
                distances[i1, i2] = distance(c1, c2)
        # Sort by euclidean distance and and store both indices of circuits and the distance (latter not used)
        distance_list = sorted(
            [(i, v) for i, v in np.ndenumerate(distances) if v > 0],
            key=lambda x: x[1],
        )
        return distances, distance_list


    distances, distance_list = calculate_distances(input_data)
    return (distance_list,)


@app.cell
def _(distance_list, input_data, math, num_connections):
    def problem_a(data):
        # Go through the first num_connections items (note: multiplied by 2, as each element will appear twice)
        circuits = []
        for d in distance_list[: 2 * num_connections]:
            i, dist = d
            # List of all junction boxes that appear in any circuit (to do quick check)
            any_circuit = [c for sublist in circuits for c in sublist]
            if i[0] in any_circuit and i[1] in any_circuit:
                # Both are in a circuit, so check if these are 2 different circuits (to be combined)
                set_to_merge = None
                for idx_c, c in enumerate(circuits):
                    if i[0] in c and i[1] in c:
                        # Both already in same circuit, ignore
                        break
                    elif i[0] in c:
                        # Only first one in circuit
                        c.add(i[1])
                        if set_to_merge is None:
                            set_to_merge = idx_c
                        else:
                            circuits[set_to_merge] = circuits[set_to_merge].union(
                                c
                            )
                            circuits[idx_c] = {}
                            break
                    elif i[1] in c:
                        # Only second one in circuit
                        c.add(i[0])
                        if set_to_merge is None:
                            set_to_merge = idx_c
                        else:
                            circuits[set_to_merge] = circuits[set_to_merge].union(
                                c
                            )
                            circuits[idx_c] = {}
                            break
            if i[0] in any_circuit or i[1] in any_circuit:
                # Only one is in a circuit - just add both to each set, should always work.
                for c in circuits:
                    if i[0] in c or i[1] in c:
                        c.add(i[0])
                        c.add(i[1])
                        break
            else:
                # Not in any circuit yet: add a new set.
                circuits.append({i[0], i[1]})

        # Product of size of 3 largest circuits
        return math.prod(sorted([len(c) for c in circuits], reverse=True)[:3])


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(distance_list, input_data):
    def problem_b(data):
        """Same as problem a, but for loop does not end at 2*num_connections.
        Instead stopping is determined by the condition that all junction boxes are in a single circuit for the first time."""
        # Go through the first num_connections items (note: multiplied by 2, as each element will appear twice)
        circuits = []
        for d in distance_list:
            i, dist = d
            # List of all junction boxes that appear in any circuit (to do quick check)
            any_circuit = [c for sublist in circuits for c in sublist]
            if i[0] in any_circuit and i[1] in any_circuit:
                # Both are in a circuit, so check if these are 2 different circuits (to be combined)
                set_to_merge = None
                for idx_c, c in enumerate(circuits):
                    if i[0] in c and i[1] in c:
                        # Both already in same circuit, ignore
                        break
                    elif i[0] in c:
                        # Only first one in circuit
                        c.add(i[1])
                        if set_to_merge is None:
                            set_to_merge = idx_c
                        else:
                            circuits[set_to_merge] = circuits[set_to_merge].union(
                                c
                            )
                            circuits[idx_c] = {}
                            break
                    elif i[1] in c:
                        # Only second one in circuit
                        c.add(i[0])
                        if set_to_merge is None:
                            set_to_merge = idx_c
                        else:
                            circuits[set_to_merge] = circuits[set_to_merge].union(
                                c
                            )
                            circuits[idx_c] = {}
                            break
            if i[0] in any_circuit or i[1] in any_circuit:
                # Only one is in a circuit - just add both to each set, should always work.
                for c in circuits:
                    if i[0] in c or i[1] in c:
                        c.add(i[0])
                        c.add(i[1])
                        break
            else:
                # Not in any circuit yet: add a new set.
                circuits.append({i[0], i[1]})

            # Stop looping, the first time that the number of circuits is 1,
            # AND the sum is equal to the number of junction boxes (so every one is included).
            if len([len(c) for c in circuits if len(c)]) == 1 and sum(
                [len(c) for c in circuits if len(c)]
            ) == len(data):
                prod_x_last_connections = data[d[0][0]][0] * data[d[0][1]][0]
                break

        return prod_x_last_connections


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
