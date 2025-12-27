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
def _(np, os, re, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        data = data.split("\n\n")
        output = {"templates": [], "areas": []}
        # Extract template areas as numpy array of ones and zeros.
        for l in data[:-1]:
            output["templates"].append(
                np.array(
                    [[1 if c == "#" else 0 for c in i] for i in l.split("\n")[1:]]
                )
            )
        # Extract areas to test
        for l in data[-1].strip().split("\n"):
            res = re.findall(r"(\d+)", l)
            output["areas"].append(
                (
                    tuple([int(r) for r in res[:2]]),
                    tuple([int(r) for r in res[2:]]),
                )
            )
        print(output)
        return output


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
def _(input_data, math):
    def first_prune(areas, data):
        """Only include areas where the sum of units fits in the area (without trying to fit)"""
        pruned_areas = []
        for a in areas:
            if math.prod(a[0]) >= sum(
                [v * data["templates"][i].sum() for i, v in enumerate(a[1])]
            ):
                pruned_areas.append(a)
        return pruned_areas


    def problem_a(data):
        """It turns out only looking at unit/square count gives the right answer, no fitting needed"""
        areas = data["areas"]
        pruned_areas = first_prune(areas, data)
        return len(pruned_areas)


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
