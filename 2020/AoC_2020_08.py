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
    return os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        data = [d.strip().split(" ") for d in data]
        data = [(d[0], int(d[1])) for d in data]
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
    def execute_program(program):
        accumulator = 0
        indices_processed = []
        idx = 0
        # Continue running until reaching inf loop (problem a) or idx after program (problem b)
        while idx not in indices_processed and idx < len(program):
            indices_processed.append(idx)
            match program[idx][0]:
                case "nop":
                    idx += 1
                case "acc":
                    accumulator += program[idx][1]
                    idx += 1
                case "jmp":
                    idx += program[idx][1]
        # Return accumulator for both problems and (final) idx for problem b
        return accumulator, idx


    def problem_a(data):
        accumulator, _ = execute_program(data)
        return accumulator


    answer_a = problem_a(input_data)
    return answer_a, execute_program


@app.cell
def _(execute_program, input_data):
    def problem_b(data):
        for idx, d in enumerate(data):
            if d[0] in ["nop", "jmp"]:
                # Swap single 'nop' or 'jmp' and run program
                data[idx] = ("nop" if d[0] == "jmp" else "jmp", d[1])
                accumulator, final_idx = execute_program(data)
                # Return data in original state to try another swap
                data[idx] = d
                # Right swap found if idx reaches the end of the program
                if final_idx >= len(data):
                    return accumulator


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
