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
        data = [d.strip() for d in data]
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
    def eval_no_brackets_a(s):
        '''Evaluate operations from left to right to ignore precedence (i.e., * has no prio over +'''
        assert '(' not in s, "No brackets allowed in this function."
        assert ')' not in s, "No brackets allowed in this function."
        parts = s.split(" ")
        answer = int(parts[0])
        for i in range(1, len(parts), 2):
            answer = eval(f"{answer}{parts[i]}{parts[i+1]}")
        return answer

    def math(s, eval_func):
        '''Evaluate expressions by running eval_func (which determines precedence) of each part between brackets'''
        # Outer brackets to make sure there are always brackets
        s = f"({s})"
        # Keep going until all brackets are gone
        while "(" in s:
            idx_last_open_bracket = None
            i = 0
            # Find closing bracket, and evaluate part between last opening and this closing bracket
            while s[i] != ")":
                if s[i] == "(":
                    idx_last_open_bracket = i
                i += 1
            # Rewrite evaluation string to replace (...) with the evaluated answer
            s = s[:idx_last_open_bracket] + str(eval_func(s[idx_last_open_bracket+1:i])) + s[i+1:]
        return int(s)
    

    def problem_a(data):
        return sum([math(d, eval_no_brackets_a) for d in data])
    answer_a = problem_a(input_data)
    return answer_a, math


@app.cell
def _(input_data, math):
    def eval_no_brackets_b(s):
        '''Evaluate such that + has presedence over *'''
        assert '(' not in s, "No brackets allowed in this function."
        assert ')' not in s, "No brackets allowed in this function."
        parts = s.split(" ")
        # Addition first; loop through all + operators
        plus_ops = [i for i, p in enumerate(parts) if p == '+']
        parts_after_addition = parts[:plus_ops[0]-1] if len(plus_ops) else parts
        for i, p in enumerate(plus_ops):
            # If last elements is a digit, it means there were two additions in a row
            if len(parts_after_addition) and parts_after_addition[-1].isdigit():
                parts_after_addition[-1] = str(int(parts_after_addition[-1])+int(parts[p+1]))
            # If the last element in parts_after_addition is not a number, it means it's a *
            else:
                parts_after_addition.append(str(int(parts[p-1])+int(parts[p+1])))
            # If there is another + operation after this one, add all original elements until that is reached
            if i+1 < len(plus_ops):
                parts_after_addition += parts[p+2:plus_ops[i+1]-1]
            # If no more plus additions, make sure the last elements of parts is added
            elif p+2 < len(parts):
                parts_after_addition += parts[p+2:]

        # Only multiplication left, so can just return normal evaluation
        return eval(' '.join(parts_after_addition)) 

    def problem_b(data):
        return sum([math(d, eval_no_brackets_b) for d in data])
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
