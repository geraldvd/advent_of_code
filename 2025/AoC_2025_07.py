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
    return np, os, sample


@app.cell
def _(np, os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # Problem-specific post-processing
        data = np.array([list(d.strip()) for d in data])
        print(data)
        return data

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data, np):
    def start_split_locations(data):
        '''Get start location (tuple(row, col)) and split locations (list of tuples)'''
        start_location = tuple(np.argwhere(data == "S")[0])
        split_locations = [tuple(c) for c in np.argwhere(data == "^")]
        return start_location, split_locations

    def problem_a(data):
        start_loc, split_locations = start_split_locations(data)
        row = start_loc[0]
        # Beam cols is a set, since duplicates due to shared splits should be ignored.
        beam_cols = {start_loc[1]}
        # Number of splits is final answer. (Note: cannot count split locations, as some may never be hit by a beam)
        num_splits = 0
        # Loop down from start location until the end
        while row < len(data):
            row += 1
            new_beam_cols = set()
            for b in beam_cols:
                if (row, b) in split_locations:
                    num_splits += 1
                    new_beam_cols.add(b+1)
                    new_beam_cols.add(b-1)
                else:
                    new_beam_cols.add(b)
            beam_cols = new_beam_cols.copy()
        return num_splits
    answer_a = problem_a(input_data)
    return answer_a, start_split_locations


@app.cell
def _(input_data, start_split_locations):
    def problem_b(data):
        start_loc, split_locations = start_split_locations(data)
        row = start_loc[0]
        # Beam cols is a dict, as all duplicates have to be kept. 
        # (Notes: technically a list, but grows too large. Dict with counts serves the same purpose.)
        beam_cols = {start_loc[1]: 1}
        # Loop down from start location until end
        while row < len(data):
            row += 1
            new_beam_cols = dict()
            for b in beam_cols.keys():
                if (row, b) in split_locations:
                    if b+1 not in new_beam_cols.keys():
                        new_beam_cols[b+1] = 0
                    if b-1 not in new_beam_cols.keys():
                        new_beam_cols[b-1] = 0
                    new_beam_cols[b+1] += beam_cols[b]
                    new_beam_cols[b-1] += beam_cols[b]
                else:
                    if b not in new_beam_cols.keys():
                        new_beam_cols[b] = 0
                    new_beam_cols[b] += beam_cols[b]
            beam_cols = new_beam_cols.copy()
        # Return value is the sum of all beam counts (timelines) per location
        return sum(beam_cols.values())
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
