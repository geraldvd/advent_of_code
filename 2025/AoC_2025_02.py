import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import math
    import re

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
    return os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        data = data[0].strip().split(",")
        data = [(int(d.split("-")[0]), int(d.split("-")[1])) for d in data]
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
    def get_all_nums(ranges):
        """Create flattened list of all numbers in all ranges"""
        all_nums = [list(range(d[0], d[1] + 1)) for d in ranges]
        return [n for sublist in all_nums for n in sublist]


    def problem_a(data):
        """A number is invalid if the first half of the digits gives the same number as the second half.
        Output: sum of the invalid numbers."""
        sum_invalid = 0
        for n in get_all_nums(data):
            s = str(n)
            # Check length of digits is even and first half of digits equals last half
            if len(s) % 2 == 0 and s[: len(s) // 2] == s[len(s) // 2 :]:
                sum_invalid += n
        return sum_invalid


    answer_a = problem_a(input_data)
    return answer_a, get_all_nums


@app.cell
def _(get_all_nums, input_data):
    def problem_b(data):
        """A number is invalid if all digits consists of a repeated pattern of digits.
        Output: sum of the invalid numbers."""
        sum_invalid = 0
        for n in get_all_nums(data):
            s = str(n)
            for i in range(2, len(s) + 1):
                if len(s) % i == 0 and s[: len(s) // i] * i == s:
                    sum_invalid += n
                    break
        return sum_invalid


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
