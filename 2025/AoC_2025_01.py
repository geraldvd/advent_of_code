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
        data = [(d.strip()[0], int(d.strip()[1:])) for d in data]
        # Right turns of dial: positive ints, left turns: negative ints
        data = [d[1] if d[0] == "R" else -d[1] for d in data]
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
    def problem_a(data):
        loc = 50
        zero_count = 0
        for d in data:
            loc += d
            # Dial is between 0 and 99. Rotate such that the arrow is in that range.
            while loc < 0:
                loc += 100
            while loc > 99:
                loc -= 100
            # Count any turn that lands at zero
            if loc == 0:
                zero_count += 1
        return zero_count


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def problem_b(data):
        loc = 50
        zero_count = 0
        # Loop through instructions
        for clicks in data:
            # Loop through each click one by one. When zero is passed at any time, increment zero_count.
            while clicks != 0:
                if clicks < 0:
                    loc -= 1
                    if loc < 0:
                        loc += 100
                    clicks += 1
                    if loc == 0:
                        zero_count += 1
                if clicks > 0:
                    loc += 1
                    if loc > 99:
                        loc -= 100
                    clicks -= 1
                    if loc == 0:
                        zero_count += 1
        return zero_count


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
