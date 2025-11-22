import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np

    # Settings
    sample = True # Fill in False, or the sample number (True and 1 are the same)
    return os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # TODO: problem-specific post-processing
        return data

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+int(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data):
    def problem_a(data):
        # TODO solve problem a
        return None
    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def problem_b(data):
        # TODO solve problem b
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
