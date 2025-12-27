import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import re
    import time
    import sympy as sp

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
    return np, os, re, sample, sp, time


@app.cell
def _(os, re, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        machines = []
        for d in data:
            res = re.findall(r"\[([\.#]+)\] ([\(\)\d\,\s]+)\{([\d\,]+)\}", d)[0]
            button_wiring = re.findall(r"\(([\d\,]+)\)\s+", res[1])
            machine = {
                "lights": [1 if s == "#" else 0 for s in res[0]],
                "button_wiring": [
                    tuple([int(i) for i in b.split(",")]) for b in button_wiring
                ],
                "joltage_req": [int(r) for r in res[2].split(",")],
            }
            machines.append(machine)
        print(machines)
        return machines


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
    def compress_list(seq):
        """Duplicates in list can be removed, since it's only toggle switches. Sort at the end.
        Example: [1,2,2,2,3,3,4] --> [1,2,4] (i.e., pairs of 2 cancel eachother)
        """
        toggle_dict = {s: seq.count(s) % 2 for s in set(seq)}
        seq_out = []
        for k in sorted(toggle_dict.keys()):
            seq_out += [k] * toggle_dict[k]
        return tuple(seq_out)


    def problem_a(data):
        total_button_presses = 0
        for machine in data:
            # Determine which lights need to be toggled an odd number of times
            # Run compress_list to allow to compare later with outcomes of button presses.
            lights_to_toggle = compress_list(
                [idx for idx, l in enumerate(machine["lights"]) if l > 0]
            )

            # Press each button 1 time and store the result in a set (to remove duplicates)
            button_sequences = set()
            for bw in machine["button_wiring"]:
                # Run compress_list to always get the same result
                button_sequences.add(compress_list(bw))

            # Keep incrementing button presses, until a sequence is found that works
            button_presses = 1
            while lights_to_toggle not in button_sequences:
                button_presses += 1
                # Add new compressed sequence to set (avoiding duplicates) for every button sequence
                new_button_sequences = set()
                for bs in button_sequences:
                    for bw in machine["button_wiring"]:
                        new_button_sequences.add(compress_list(bs + bw))
                button_sequences = new_button_sequences.copy()

            # Button presses found, add to total
            total_button_presses += button_presses

        return total_button_presses


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data, np, sp, time):
    def optimize_linear_equation(d):
        t0 = time.time()
        # Create A and b for linear algebra format Ax=b
        m, n = len(d["joltage_req"]), len(d["button_wiring"])
        A = np.zeros((m, n), dtype=np.int64)
        for idx, bw in enumerate(d["button_wiring"]):
            for bwi in bw:
                A[bwi, idx] = 1
        b = np.array(d["joltage_req"], dtype=np.int64).reshape(-1, 1)

        # Convert to sympy system for solving symbolically
        A_sp = sp.Matrix(A)
        b_sp = sp.Matrix(b)

        # Starting point (INF) and constants
        best_solution = 1e100
        ERR = 1e-4
        LOWER_BOUND = 0
        UPPER_BOUND = 200

        # Create xi variables based; number of vars dependent on rank of the system.
        x_s = sp.symbols(f"x0:{A.shape[1]}", integer=True)

        # Solve the linear system and assert there is a solution (which is the case for all advent of code problems)
        sol = tuple(sp.linsolve((A_sp, b_sp), x_s))
        assert len(sol) > 0, (
            "There should at least be a solution to the system of linear equations."
        )
        sol = sol[0]

        # Extract the free variables. I.e., the one that need to be optimized (brute force below)
        free_vars = [v for v, expr in zip(x_s, sol) if expr == v]

        # To simplify the brute force below, assume there is a max of 3 variables (which is the case for my problem set)
        assert len(free_vars) <= 3, "Assumed max 3 free variables"

        # Unique solution, so no free variables
        if not len(free_vars):
            return sum(sol)
        # Multiple solutions, dependent on variables in free_vars
        else:
            # Create a function that's efficient to evaluate when looping over many possible values
            func = sp.lambdify(free_vars, sol, modules="sympy")

        # Single variable
        if len(free_vars) == 1:
            for u in range(LOWER_BOUND, UPPER_BOUND):
                vals = [round(i, 1) for i in func(u)]
                if (
                    all(abs(int(val) - val) < ERR and val >= 0 for val in vals)
                    and sum(vals) < best_solution
                ):
                    best_solution = sum(vals)
            return best_solution
        # 2 variables
        elif len(free_vars) == 2:
            for u in range(LOWER_BOUND, UPPER_BOUND):
                for v in range(LOWER_BOUND, UPPER_BOUND):
                    vals = [round(i, 1) for i in func(u, v)]
                    if (
                        all(abs(int(val) - val) < ERR and val >= 0 for val in vals)
                        and sum(vals) < best_solution
                    ):
                        best_solution = sum(vals)
            return best_solution
        # 3 variables; assertion above guarantees this is the only option left.
        else:
            for u in range(LOWER_BOUND, UPPER_BOUND):
                for v in range(LOWER_BOUND, UPPER_BOUND):
                    for w in range(LOWER_BOUND, UPPER_BOUND):
                        vals = [round(i, 1) for i in func(u, v, w)]
                        if (
                            all(
                                abs(int(val) - val) < ERR and val >= 0
                                for val in vals
                            )
                            and sum(vals) < best_solution
                        ):
                            best_solution = sum(vals)
            return best_solution


    def problem_b(data):
        t0 = time.time()
        sum_solution = 0
        total_invalid = 0

        for d_idx, d in enumerate(data):
            best_solution = optimize_linear_equation(d)
            sum_solution += best_solution
            if best_solution > 1e99:
                total_invalid += 1
            print(f"{d_idx + 1}/{len(data)}", best_solution)
        print()
        print(
            f"Solved in {time.time() - t0} seconds. Solution: {sum_solution} with {total_invalid} invalid results."
        )
        return sum_solution


    answer_b = problem_b(input_data)
    return (answer_b,)


@app.cell(hide_code=True)
def _(answer_a, answer_b, day_number):
    # Show answers
    print(f"Day {int(day_number)}a: {answer_a if answer_a else '-'}")
    print(f"Day {int(day_number)}b: {answer_b if answer_b else '-'}")
    return


if __name__ == "__main__":
    app.run()
