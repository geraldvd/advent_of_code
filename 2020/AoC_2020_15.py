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
        data = [int(d) for d in data[0].split(',')]
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
    def problem_a(data, final_turn=2020):
        '''Don't use full list, but hash-map, to allow much larger final numbers (apparently problem b)'''
        # Create dicts of last two times number was mentioned, with the number as key and turn id as value
        last_spoken_map = {}
        second_last_spoken_map = {}

        # Go through initial numbers
        turn = 1
        last_number = None
        for d in data:
            last_number = d
            if d in last_spoken_map.keys():
                second_last_spoken_map[d] = last_spoken_map[d]
            last_spoken_map[d] = turn
            turn += 1

        # Continue with turns until desired final turn
        while turn <= final_turn:
            # If last number was spoken for the first time, the new number will be zero
            if last_number not in second_last_spoken_map.keys():
                second_last_spoken_map[0] = last_spoken_map[0]
                last_spoken_map[0] = turn
                last_number = 0
            # If last number was spoken before, take difference in turn number of last time and time before that
            else:
                new_number = last_spoken_map[last_number] - second_last_spoken_map[last_number]
                if new_number in last_spoken_map.keys():
                    second_last_spoken_map[new_number] = last_spoken_map[new_number]
                last_spoken_map[new_number] = turn
                last_number = new_number
            turn += 1
    
        return last_number
    answer_a = problem_a(input_data)
    return answer_a, problem_a


@app.cell
def _(input_data, problem_a):
    def problem_b(data):
        return problem_a(data, final_turn=30000000)
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
