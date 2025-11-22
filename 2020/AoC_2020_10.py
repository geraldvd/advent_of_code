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
    sample = 2 # Fill in False, or the sample number (True and 1 are the same)
    return math, np, os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # Problem-specific post-processing
        data = [int(d.strip()) for d in data]
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
    def calculate_jolt_list(data):
        # Jolt jump counters. 3 jolt is initialized as 1 to account for final jump
        differences = {1: 0, 2: 0, 3: 1}
        jolt = 0
        jolt_seq = [jolt] # Note: only as helper for problem b, not needed for a
        while jolt < max(data):
            # Check closest jolt above current and stop when first reached
            for i in range(1, 4):
                if jolt + i in data:
                    differences[i] += 1
                    jolt = jolt + i
                    jolt_seq.append(jolt)
                    break
        return differences, jolt_seq

    def problem_a(data):
        differences, _ = calculate_jolt_list(data)
        print(differences)
        return differences[1] * differences[3]
    answer_a = problem_a(input_data)
    return answer_a, calculate_jolt_list


@app.cell
def _(calculate_jolt_list, input_data, math, np):
    def problem_b(data):
        _, jolt_seq = calculate_jolt_list(data)
        print(jolt_seq)
        seq = np.array(jolt_seq[1:]) - np.array(jolt_seq[:-1])
        count_single_increments = [len(i) for i in ''.join([str(s) for s in seq]).split('3') if len(i) > 1]
        print(count_single_increments)
        print(math.prod([c+1 if c > 2 else c for c in count_single_increments]))
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
    2**3
    return


@app.cell
def _(math):
    math.comb(4, 2)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
