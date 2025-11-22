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
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # TODO: problem-specific post-processing
        data = [int(d) for d in data]
        return data

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+int(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())
    
    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data, np):
    def problem_a(data):
        # Create square matrix with repeated data columns
        expense_matrix = np.array(data*len(data)).reshape((len(data), len(data)))
        # Find coordinates of elements where sum is 2020 (note: 2 results, inversed indices)
        idx_matching = np.argwhere(expense_matrix.transpose() + expense_matrix == 2020)[0]
        # Return product of the data points at the indices
        return data[idx_matching[0]] * data[idx_matching[1]]
    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def problem_b(data):
        # Loop through the data 3 times to solve
        for i in data:
            for j in data:
                for k in data:
                    if i+j+k == 2020:
                        return i*j*k
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
