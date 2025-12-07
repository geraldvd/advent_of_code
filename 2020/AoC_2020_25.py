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
        card, door = int(data[0].strip()), int(data[1].strip())
        data = {"card": card, "door": door}
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
    def transform(subject_number, loop_size):
        value = 1
        for i in range(1, loop_size+1):
            # Set the value to itself multiplied by the subject number.
            value *= subject_number
            # Set the value to the remainder after dividing the value by 20201227.
            value %= 20201227
        return value

    def problem_a(data):
        subject_number = 7
        # Determine card loop size
        loop_size_card = 0
        value = 1
        while value != data["card"]:
            loop_size_card += 1
            value = transform(subject_number, loop_size_card)
        # Determine door loop size
        loop_size_door = 0
        value = 1
        while value != data["door"]:
            loop_size_door += 1
            value = transform(subject_number, loop_size_door)
        
        # Return encryption key after checking the one from card and door are equal
        assert transform(data["door"], loop_size_card) == transform(data["card"], loop_size_door), \
            "Encryption key for door and card must be the same"
        return transform(data["door"], loop_size_card)
    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def problem_b(data):
        # TODO solve problem b
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
    return


if __name__ == "__main__":
    app.run()
