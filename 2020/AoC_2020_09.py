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
        data = np.array([int(d.strip()) for d in data])
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
def _(input_data, sample):
    def problem_a(data):
        # Num. preamble numbers of sample problem is 5, while real one is 25
        n_preamble = 5 if sample else 25
        # Sum_list always contains n_preamble numbers before idx
        sum_list = data[:n_preamble]
        idx = n_preamble
        while True:
            num = data[idx]
            # Return from the function if no two numbers in sum_list sum up to num
            remainder_list = num - sum_list
            if not bool(
                [True for r in remainder_list if r in sum_list and r != num]
            ):
                return num
            # Set new idx and sum_list
            idx += 1
            sum_list = data[idx - n_preamble : idx]


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(answer_a, input_data):
    def problem_b(data):
        start_idx = 0
        while True:
            sum_list = []
            idx = start_idx
            while sum(sum_list) < answer_a:
                sum_list.append(data[idx])
                idx += 1
            if sum(sum_list) == answer_a:
                return min(sum_list) + max(sum_list)
            start_idx += 1


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
