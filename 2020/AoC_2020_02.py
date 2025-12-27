import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
    return np, os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        cleaned_data = []
        for d in data:
            d = d.split(" ")
            cd = {
                "min_count": int(d[0].split("-")[0]),
                "max_count": int(d[0].split("-")[1]),
                "letter": d[1].strip(":"),
                "password": d[2].strip(),
            }
            cleaned_data.append(cd)
        return cleaned_data


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
def _(input_data, np):
    def problem_a(data):
        num_valid_passwords = 0
        for d in data:
            letter_count = len(
                np.argwhere(np.array(list(d["password"])) == d["letter"])
            )
            if d["min_count"] <= letter_count <= d["max_count"]:
                num_valid_passwords += 1
        return num_valid_passwords


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def problem_b(data):
        num_valid_passwords = 0
        for d in data:
            idx_1 = d["min_count"] - 1
            idx_2 = d["max_count"] - 1
            p = d["password"]
            l = d["letter"]
            if (
                (idx_1 < len(p) and p[idx_1] == l)
                or (idx_2 < len(p) and p[idx_2] == l)
            ) and (idx_1 < len(p) and idx_2 < len(p) and p[idx_1] != p[idx_2]):
                num_valid_passwords += 1
        return num_valid_passwords


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
