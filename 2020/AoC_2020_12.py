import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np

    # Settings
    sample = False # Fill in False, or the sample number (True and 1 are the same)
    return os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # Problem-specific post-processing
        data = [(d.strip()[0],int(d.strip()[1:])) for d in data]
        assert not sum([s%90 for s in set([d[1] for d in data if d[0] in ['R', 'L']])]), \
                'Program expects rotations to be multiples of 90 deg'
        return data

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data):
    def problem_a(data):
        lookup = {'N': 0, 'E': 90, 'S': 180, 'W': 270, 'R': +1, 'L': -1}
        dir = lookup['E']
        loc = {lookup['N']: 0, lookup['E']: 0, lookup['S']: 0, lookup['W']: 0}
        for d in data:
            # Rotoate ship
            if d[0] in ['R', 'L']:
                dir += lookup[d[0]] * d[1]
            # Move ship forward in current direction
            elif d[0] == 'F':
                loc[dir] += d[1]
            # Move ship N, E, S, W
            else:
                loc[lookup[d[0]]] += d[1]
            # Fix negative direction
            if dir < 0:
                dir += 360
            if dir > 270:
                dir -= 360
        return abs(loc[lookup['S']] - loc[lookup['N']]) + abs(loc[lookup['E']] - loc[lookup['W']])
    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def problem_b(data):
        lookup = {'N': 0, 'E': 90, 'S': 180, 'W': 270, 'R': +1, 'L': -1}
        # Waypoint loc is relative to ship, loc is ship location
        waypoint_loc = {lookup['N']: 1, lookup['E']: 10, lookup['S']: 0, lookup['W']: 0}
        loc = {lookup['N']: 0, lookup['E']: 0, lookup['S']: 0, lookup['W']: 0}
        for d in data:
            # Rotate waypoint around ship
            if d[0] in ['R', 'L']:
                new_waypoint_loc = {}
                rotation = lookup[d[0]] * d[1]
                for k in waypoint_loc.keys():
                    k_new = k + rotation
                    if k_new < 0: 
                        k_new += 360
                    elif k_new >= 360:
                        k_new -= 360
                    new_waypoint_loc[k_new] = waypoint_loc[k]
                waypoint_loc = new_waypoint_loc
            # Move ship by scaling distance between waypoint and ship
            elif d[0] == 'F':
                for k in waypoint_loc.keys():
                    loc[k] += d[1]*waypoint_loc[k]
            # Move waypoint N, E, S, W
            else:
                waypoint_loc[lookup[d[0]]] += d[1]
        return abs(loc[lookup['S']] - loc[lookup['N']]) + abs(loc[lookup['E']] - loc[lookup['W']])
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
