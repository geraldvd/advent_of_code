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
    return np, os, re, sample


@app.cell
def _(np, os, re, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        lines = []
        for d in data[:-1]:
            lines.append([int(i) for i in re.findall(r"(\d+)\s+", d)])
        operators = re.findall(r"([*+]+)\s+", data[-1])
        data = {
            "lines": np.array(lines),
            "operators": operators,
            "raw_lines": [d.strip("\n") for d in data[:-1]],
        }
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
        """Simply extract numbers with regular expressions (in post process function ) and apply operator."""
        sum_answers = 0
        for i, o in enumerate(data["operators"]):
            answer = (
                data["lines"][:, i].prod()
                if o == "*"
                else data["lines"][:, i].sum()
            )
            sum_answers += answer
        return sum_answers


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data, np):
    def problem_b(data):
        """Go through the strings digit by digit and build up the numbers.
        If whitespaces in each line align, it means operator can be applied."""
        sum_answers = 0
        operators = data["operators"].copy()
        nums = []
        for j in range(len(data["raw_lines"][0])):
            num = ""
            all_whitespace = True
            for i in range(len(data["raw_lines"])):
                if data["raw_lines"][i][j].isdigit():
                    all_whitespace = False
                    num += data["raw_lines"][i][j]
            if num.strip().isdigit():
                nums.append(int(num.strip()))
            if all_whitespace or j == len(data["raw_lines"][0]) - 1:
                nums = np.array(nums)
                o = operators.pop(0)
                answer = nums.prod() if o == "*" else nums.sum()
                sum_answers += answer
                nums = []
        return sum_answers


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
