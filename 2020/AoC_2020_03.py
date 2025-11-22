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
        # Create 2D numpy array with True at each tree location
        data = [list(d.strip()) for d in data]
        data = np.array(data) == '#'
        return data

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data, np):
    def problem_a(data : np.ndarray, step=(1,3)):
        pos = (0,0)
        tree_count = 0
        while pos[0] < data.shape[0]:
            # Add 1 to tree count if pos is on a tree
            tree_count += data[pos]
            # Update position by jumping 1 down and 3 right
            pos = (pos[0]+step[0], pos[1]+step[1])
            # Handle horizontally repeated pattern, by jumping back left when on right edge of map
            if pos[1] >= data.shape[1]:
                pos = (pos[0], pos[1] - data.shape[1])
        return tree_count
    answer_a = problem_a(input_data)
    return answer_a, problem_a


@app.cell
def _(input_data, np, problem_a):
    def problem_b(data):
        # Same as problem a, but multiplying different steps
        steps = [
            (1,1), # Right 1, down 1.
            (1,3), # Right 3, down 1.
            (1,5), # Right 5, down 1.
            (1,7), # Right 7, down 1.
            (2,1), # Right 1, down 2.
        ]
        return np.prod([problem_a(data, s) for s in steps])
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
