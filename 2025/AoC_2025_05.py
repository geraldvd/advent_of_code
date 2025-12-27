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
        data = data.strip().split("\n\n")
        ranges = [
            tuple([int(i) for i in d.split("-")]) for d in data[0].split("\n")
        ]
        ingredients = [int(d) for d in data[1].split("\n")]
        data = {"fresh_ranges": ranges, "ingredients": ingredients}
        print(data)
        return data


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
def _(input_data):
    def problem_a(data):
        num_fresh = 0
        for i in data["ingredients"]:
            for r in data["fresh_ranges"]:
                if i in range(r[0], r[1] + 1):
                    num_fresh += 1
                    break
        return num_fresh


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def problem_b(data):
        # Sort ranges first by first (smaller) element and then second (larger) element.
        ranges = sorted(data["fresh_ranges"], key=lambda i: (i[0], i[1]))
        total_fresh = 0
        # Max_r is the right-most bound considered. You never should move back below that.
        max_r = -1
        for r in ranges:
            if r[0] > max_r:
                # Entire range to be added
                total_fresh += r[1] - r[0] + 1
                max_r = r[1]
            elif r[1] >= max_r:
                # Add only range between current max_r and r_1 (new max_r)
                total_fresh += r[1] - max_r
                max_r = r[1]
        return total_fresh


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
