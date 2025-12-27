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
        # Set roll locations to True
        data = np.array(
            [[True if l == "@" else False for l in row.strip()] for row in data]
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
    def problem_a(data):
        roll_coords = {tuple(r) for r in np.argwhere(data)}
        accessible_rolls = 0
        for r in roll_coords:
            # Count roll as accesssible if <4 rolls are adjacent
            adj_rolls = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == j == 0:
                        continue
                    c = (r[0] + i, r[1] + j)
                    if c in roll_coords:
                        adj_rolls += 1
            if adj_rolls < 4:
                accessible_rolls += 1
        return accessible_rolls


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data, np, remove_idx):
    def problem_b(data):
        roll_coords = {tuple(r) for r in np.argwhere(data)}
        rolls_removed = 0

        # Run at least once (rolls_removed > 0) and then until there are no more accessible rolls
        while rolls_removed == 0 or len(remove_idx):
            remove_idx = set()
            # Identify which rolls are accessible
            for r in roll_coords:
                adj_rolls = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if i == j == 0:
                            continue
                        c = (r[0] + i, r[1] + j)
                        if c in roll_coords:
                            adj_rolls += 1
                if adj_rolls < 4:
                    remove_idx.add(r)
            # Remove rolls and count them
            rolls_removed += len(remove_idx)
            for idx in remove_idx:
                roll_coords.remove(idx)
        return rolls_removed


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
