import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import time

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
    return os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        wires = dict()
        for d in data:
            kv = d.strip().split(": ")
            wires[kv[0]] = kv[1].strip().split(" ")
        print(wires)
        return wires


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
    def count_paths(data, from_key="you", to_key="out"):
        # Avoid error if the start key does not exist
        if from_key not in data.keys():
            return None
        # Keys is what needs to be searched in next step. Start with <from_key>
        # Note: dict needed to make sure keys doesn't grow to fast. (Needed for b.)
        keys = {from_key: 1}
        paths = dict()
        # Loop until keys is empty. Note: <to_key> is never added to keys
        while len(keys.keys()):
            new_keys = {}
            for k in keys.keys():
                # Some keys might not have a key (e.g., "out"); ignore.
                if k in data.keys():
                    for k2 in data[k]:
                        if k2 not in paths.keys():
                            paths[k2] = 0
                        paths[k2] += keys[k]
                        if k2 != to_key:
                            if k2 not in new_keys.keys():
                                new_keys[k2] = 0
                            new_keys[k2] += keys[k]
            keys = new_keys.copy()
        # All paths led to <to_key> --> Return the count
        return paths[to_key] if to_key in paths else 0


    def problem_a(data):
        path_count = count_paths(data, "you", "out")
        return path_count


    answer_a = problem_a(input_data)
    return answer_a, count_paths


@app.cell
def _(count_paths, input_data):
    def problem_b(data):
        # Use the function for part a to calculate the possible routes, by multiplying the subpaths.
        route_svr_dac_fft_out = (
            count_paths(data, "svr", "dac")
            * count_paths(data, "dac", "fft")
            * count_paths(data, "fft", "out")
        )
        route_svr_fft_dac_out = (
            count_paths(data, "svr", "fft")
            * count_paths(data, "fft", "dac")
            * count_paths(data, "dac", "out")
        )
        print(f"svr -> dac -> fft -> out = {route_svr_dac_fft_out}")
        print(f"svr -> fft -> dac -> out = {route_svr_fft_dac_out}")
        # Add up the routes as result (note: in practice one is 0)
        return route_svr_dac_fft_out + route_svr_fft_dac_out


    answer_b = problem_b(input_data)
    return (answer_b,)


@app.cell
def _(answer_a, answer_b, day_number):
    # Show answers
    print(f"Day {int(day_number)}a: {answer_a if answer_a else '-'}")
    print(f"Day {int(day_number)}b: {answer_b if answer_b else '-'}")
    return


if __name__ == "__main__":
    app.run()
