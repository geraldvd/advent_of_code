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
    sample = False # Fill in False, or the sample number (True and 1 are the same)
    return math, os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        #Problem-specific post-processing
        data = [d.strip() for d in data]
        data = int(data[0]), data[1].split(',')
        print(data)
        print(len(data[1]))
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
        # Calculate tuple of bus IDs and wait time from arrival time at bus stop.
        minutes = [(int(x), int(x) - data[0]%int(x)) for x in data[1] if x.isdigit()]
        # Return bus ID multiplied with min. num minutes to wait (that's the minimum of the modulo calculated above).
        return math.prod(min(minutes, key=lambda item: item[1]))
    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data, math):
    def test_times(start, bus_intervals, offsets, increment=1):
        num = start
        while sum([(num+offsets[i])%bus_intervals[i] for i, _ in enumerate(bus_intervals)]):
            num += increment
        return num

    def problem_b(data):
        '''
        Hint used: https://www.reddit.com/r/adventofcode/comments/kc60ri/2020_day_13_can_anyone_give_me_a_hint_for_part_2/gfpqdm3/
        Underlying theorem: Chinese Remainder Theorem.
        '''
        # Extract bus intervals and offsets (i.e., T+offset needs to be used to find T)
        bus_intervals = [int(x) for x in data[1] if x.isdigit()]
        offsets = [i for i, x in enumerate(data[1]) if x.isdigit()]
        print(bus_intervals, offsets)

        # Start searching at 0. First use 2 buses, and update the starting point.
        # The increment is always the product of the bus intervals (valid because they are co-primes).
        # This means the jumps will get larger, to reduce search space.
        # For the increment, I needed the hint from Reddit.
        num = 0
        for i in range(1, len(bus_intervals)):
            increment = math.prod(bus_intervals[:i])
            num = test_times(num, bus_intervals[:i+1], offsets[:i+1], increment)
            print(f"First valid T for buses {', '.join([str(n) for n in bus_intervals[:i+1]])}: {num} "\
                  f"(=next starting num, interval is {math.prod(bus_intervals[:i+1])})")
        return num
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
