import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np

    # Settings
    sample = 0 # Fill in False, or the sample number (True and 1 are the same)
    return np, os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # Problem-specific post-processing
        return [d.strip() for d in data]

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data):
    def calc_seat_id(d):
        # Determine row - binary first 7 digits
        row = sum([int(b)*2**(len(d[:7])-idx-1) for \
                   idx,b in enumerate(d[:7].replace('F', '0').replace('B', '1'))])
        # Determine seat - binary last 3 digits
        seat = sum([int(b)*2**(len(d[7:])-idx-1) for \
                    idx,b in enumerate(d[7:].replace('L', '0').replace('R', '1'))])
        return 8*row + seat

    def problem_a(data):
        max_seat_id = 0
        for d in data:
            seat_id = calc_seat_id(d)
            max_seat_id = seat_id if seat_id > max_seat_id else max_seat_id
        return max_seat_id
    answer_a = problem_a(input_data)
    return answer_a, calc_seat_id


@app.cell
def _(calc_seat_id, input_data, np):
    def problem_b(data):
        # Calculate all seat ids on the plane in order
        seat_ids = np.array(sorted([calc_seat_id(d) for d in data]))
        # The only element that has a delta of 2 (i.e., missing seat) is the one
        idx = np.argwhere(seat_ids[1:] - seat_ids[:-1] == 2)[0][0]
        # Return the seat right after the found seat (since that's the one missing)
        return seat_ids[idx] + 1
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
