import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np

    # Settings
    sample = True # Fill in False, or the sample number (True and 1 are the same)
    return os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # Problem-specific post-processing
        data = [int(i) for i in data.strip()]
        print(data)
        return data

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").read())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data):
    def move(cups):
        '''
        The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
        The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
        The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
        The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        '''
        # The crab picks up the three cups that are immediately clockwise of the current cup. 
        # They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
        pick_ups = cups[1:4]
        # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. 
        # If this would select one of the cups that was just picked up, the crab will keep subtracting one until 
        # it finds a cup that wasn't just picked up. If at any point in this process the value goes below the 
        # lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
        destination = cups[0] - 1
        while destination in pick_ups or destination < min(cups):
            if destination < min(cups):
                destination = max(cups)
            else:
                destination -= 1
        dest_idx = cups.index(destination)
        # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. 
        # They keep the same order as when they were picked up.
        # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        # Note: current cup is always placed at the front (unlike the example)
        return cups[4:dest_idx+1] + pick_ups + cups[dest_idx+1:] + cups[:1]


    def problem_a(data):
        cups = data.copy()
        for i in range(100):
            cups = move(cups)
            print(cups)
        # Resequence such that the cup after 1 comes first, and does not include 1 at the end
        return ''.join([str(i) for i in cups[cups.index(1)+1:] + cups[:cups.index(1)]])
    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def problem_b(data):
        # cups = data.copy() + list(range(max(data)+1, 1000001-len(data)))
        # for i in range(1000):
            # cups = move(cups)
        print(data)
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
    a = [1,2,3]
    print(a[:1])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
