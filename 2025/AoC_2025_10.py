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
    import sys
    import sympy as sp

    # Settings
    sample = False # Fill in False, or the sample number (True and 1 are the same)
    return np, os, re, sample, sp


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
            machine = {"lights": [1 if s == "#" else 0 for s in res[0]], \
                       "button_wiring": [tuple([int(i) for i in b.split(',')]) for b in button_wiring], \
                       "joltage_req": [int(r) for r in res[2].split(',')]}
            machines.append(machine)
        print(machines)
        return machines

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data):
    def compress_list(seq):
        '''Duplicates in list can be removed, since it's only toggle switches. Sort at the end.
        Example: [1,2,2,2,3,3,4] --> [1,2,4] (i.e., pairs of 2 cancel eachother)
        '''
        toggle_dict = {s: seq.count(s)%2 for s in set(seq)}
        seq_out = []
        for k in sorted(toggle_dict.keys()):
            seq_out += [k] * toggle_dict[k]
        return tuple(seq_out)


    def problem_a(data):
        total_button_presses = 0
        for machine in data:
            # Determine which lights need to be toggled an odd number of times
            # Run compress_list to allow to compare later with outcomes of button presses.
            lights_to_toggle = compress_list([idx for idx, l in enumerate(machine["lights"]) if l > 0])


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
def _(input_data, np, sp):
    def increase_joltages(cur_joltages, added_button_wiring):
        new_joltages = list(cur_joltages)
        for bw in added_button_wiring:
            new_joltages[bw] += 1
        return tuple(new_joltages)


    def problem_b(data):
        # total_button_presses = 0
        # for machine in data[:2]:
        #     t0 = time.time()
        #     loop_count = 0
        #     # Determine which lights need to be toggled an odd number of times
        #     # Run compress_list to allow to compare later with outcomes of button presses.
        #     output_joltages = tuple(machine["joltage_req"])


        #     # Press each button 1 time and store the result in a set (to remove duplicates)
        #     button_sequences = set()
        #     for bw in machine["button_wiring"]:
        #         # Run compress_list to always get the same result
        #         initial_joltage = [0] * len(output_joltages)
        #         button_sequences.add(increase_joltages(initial_joltage, bw))
        #         loop_count += 1

        #     # Keep incrementing button presses, until a sequence is found that works
        #     button_presses = 1
        #     while output_joltages not in button_sequences:
        #         button_presses += 1
        #         # Add new compressed sequence to set (avoiding duplicates) for every button sequence
        #         new_button_sequences = set()
        #         for bs in button_sequences:
        #             for bw in machine["button_wiring"]:
        #                 new_joltages = increase_joltages(bs, bw)
        #                 loop_count += 1
        #                 # Try to reduce set size
        #                 if not sum([new_joltage>output_joltages[idx] for idx, new_joltage in enumerate(new_joltages)]):
        #                     new_button_sequences.add(new_joltages)
        #                     if new_joltages == output_joltages:
        #                         break
        #         button_sequences = new_button_sequences.copy()
        #     print(f"list length: {len(new_button_sequences)}, loop count: {loop_count}, " \
        #           f"size in memory: {sys.getsizeof(new_button_sequences)/1000} kB, took {time.time()-t0} sec.")

        #     # Button presses found, add to total
        #     total_button_presses += button_presses
        #     # print(button_presses, len(button_sequences))

        # return total_button_presses
        sum_solution = 0
        total_invalid = 0
        for d_idx, d in enumerate(data):
            # Create A and b for linear algebra format Ax=b
            m, n = len(d['joltage_req']), len(d['button_wiring'])
            A = np.zeros((m, n))
            for idx, bw in enumerate(d['button_wiring']):
                for bwi in bw:
                    A[bwi, idx] = 1
            b = np.array(d['joltage_req']).reshape(-1, 1)

            # Compute row reduced echelon form of [A|b].
            A_sp = sp.Matrix(A)
            b_sp = sp.Matrix(b)
            Ab_sp = A_sp.row_join(b_sp)
            Ab_rref, pivot_cols = Ab_sp.rref()
            Ab_rref = np.array(Ab_rref).astype(np.float64)

            # Pivot columns are columns that are fixed to a single x.
            # Free cols defines which columns are free variables (and are any column that's not pivot)
            free_cols = [c for c in range(Ab_sp.shape[1]-1) if c not in pivot_cols]

            # The entire solution space for x is: x = a + s[0]*f[0] + (...) + s[j]*f[j]
            # Where a is defined by the pivot columns and f[j] by the number of free variables
            a = n * [0]
            f = np.zeros((len(free_cols), n))
            counter = 0
            for idx in range(n):
                if idx in pivot_cols:
                    a[idx] = Ab_rref[counter, -1]
                    for f_idx in range(len(free_cols)):
                        f[f_idx, idx] = -Ab_rref[counter, free_cols[f_idx]]
                    counter += 1
            for idx, f_idx in enumerate(free_cols):
                f[idx, f_idx] = 1

            # Convert to numpy array and list of numpy arrays
            a = np.array(a).reshape(-1, 1)

            # Find optimal solution by adjusting s[j], until minimum x is found.
            # num_iter = 1000 // (len(f)+1)
            num_iter = 100 if len(f) == 3 else 1000
            best_solution = 1e100
            for i in range(num_iter**len(f)):
                mult = np.array([int(i/num_iter**j)%num_iter for j in range(len(f))]).reshape(-1, 1)
                res = a + np.dot(f.T, mult)
                if np.abs(res).sum() == res.sum() and np.round(res).sum() == res.sum() and res.sum() < best_solution:
                    best_solution = res.sum()
            sum_solution += best_solution
            if best_solution > 1e99:
                total_invalid += 1
            print(f"{d_idx+1}/{len(data)}", best_solution)
            if len(f) == 3:
                print(a)
                print(f)
                print(num_iter, mult)
                # break
        print()
        print(sum_solution, total_invalid)


    answer_b = problem_b(input_data) # 19576 is too high, tried with 300 tries
    return (answer_b,)


@app.cell
def _(answer_a, answer_b, day_number):
    # Show answers
    print(f"Day {int(day_number)}a: {answer_a if answer_a else '-'}")
    print(f"Day {int(day_number)}b: {answer_b if answer_b else '-'}")
    return


@app.cell
def _(np):
    test = np.ones((1,1))
    np.dot(np.empty((0,0)), test)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
