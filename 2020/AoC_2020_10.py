import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import math

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
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
    def calculate_jolt_list(data):
        # Jolt jump counters. 3 jolt is initialized as 1 to account for final jump
        differences = {1: 0, 2: 0, 3: 1}
        jolt = 0
        jolt_seq = [jolt]  # Note: only as helper for problem b, not needed for a
        while jolt < max(data):
            # Check closest jolt above current and stop when first reached
            for i in range(1, 4):
                if jolt + i in data:
                    differences[i] += 1
                    jolt = jolt + i
                    jolt_seq.append(jolt)
                    break
        jolt_seq.append(jolt_seq[-1] + 3)
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
        """General strategy: look at the combinations possible with multiple single digit jumps, since in-between numbers can be left out. In the problem at hand, these are the only cases to consider:
        # 1, 4, 5, 6, 9 -- (len of single diffs: 2) -- 2 combinations: 1) as-is, 2) leaving out 5
        # 1, 4, 5, 6, 7, 10 -- (len of single diffs: 3) -- 4 combinations: 1) as-is, 2-3) leaving out 5 or 6, 4) leaving out 5 and 6
        # 1, 4, 5, 6, 7, 8, 11 -- (len of single diffs: 4) -- 7 combinations: 1) as-is, 2-4) leaving out 1 of 5-7, 5-7) leaving out 2 of 5-7
        """
        _, jolt_seq = calculate_jolt_list(data)
        # Calculate jolt step sizes and isolate groups of 1 step (as there are the opportunities to leave adapters out)
        seq = np.array(jolt_seq[1:]) - np.array(jolt_seq[:-1])
        count_single_increments = [
            len(i) for i in "".join([str(s) for s in seq]).split("3") if len(i) > 1
        ]
        print(count_single_increments)
        # Use combinations in function docstring
        comb_lookup = {2: 2, 3: 4, 4: 7}
        return math.prod([comb_lookup[c] for c in count_single_increments])


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
