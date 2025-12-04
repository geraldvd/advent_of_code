import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import math

    # Settings
    sample = True # Fill in False, or the sample number (True and 1 are the same)
    return math, os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # TODO: problem-specific post-processing
        data = [d.strip() for d in data]
        data = int(data[0]), data[1].split(',')
        print(data)
        return data

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data, math):
    def problem_a(data):
        minutes = [(int(x), int(x) - data[0]%int(x)) for x in data[1] if x.isdigit()]
        return math.prod(min(minutes, key=lambda item: item[1]))
    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def test_condition(dep_sched, t):
        return sum([(t+i)%int(d) for i,d in enumerate(dep_sched) if d.isdigit()]) == 0

    def problem_b(data):
        # t = 0
        # step_size = int(data[1][0])
        # while not test_condition(data[1], t):
        #     t += step_size
        # return t
        relevant_data = []
        for i, d in enumerate(data[1]):
            if d.isdigit():
                relevant_data.append((i, int(d)))
        print(relevant_data)
        t_step = max(relevant_data, key=lambda x: x[1])[1]
        for t in range(0, 1000, 1):
            for rd in relevant_data:
                print((t+rd[0])%rd[1], end=" ")
            print()
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
