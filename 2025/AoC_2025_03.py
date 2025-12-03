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
    return os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # Problem-specific post-processing
        data = [d.strip() for d in data]
        print(data)
        return data

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data):
    def find_max_joltage_2digits(b):
        '''Go through all numbers from 100 to 10, until the largest possible number is found in right sequence.'''
        for num in range(99, 10, -1):
            s_num = str(num)
            if s_num[0] in b:
                i0 = b.index(s_num[0])
                if s_num[1] in b[i0+1:]:
                    return num

    def problem_a(data):
        return sum([find_max_joltage_2digits(d) for d in data])
    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def find_max_joltage(b, num_digits=12):
        '''Numbers to large to follow approach in problem a. Instead, find digit by digit until b has a length of num_digits (12)'''
        output = ""    
        b_remaining = b
        # Go through each position of output
        for pos in range(num_digits):
            # Loop from 9 to 0 to find the next largest digit in the remaining b string. 
            # Key fact is that currently more significant digits always have most impact on output.
            digit = 9
            s_d = str(digit)
            while True:
                if s_d in b_remaining:
                    i = b_remaining.index(s_d)
                    # Make sure b_remaining always has enough digits left for rest of number.
                    if len(b_remaining[i+1:]) >= num_digits-len(output)-1:
                        output = output + s_d
                        b_remaining = b_remaining[i+1:]
                        break
                # Try lower digit
                digit -= 1
                s_d = str(digit)
        return int(output) if output else 0

    def problem_b(data):
        return sum([find_max_joltage(d, 12) for d in data])
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
