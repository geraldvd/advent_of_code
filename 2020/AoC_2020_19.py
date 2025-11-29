import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import re
    import itertools

    # Settings
    sample = 2 # Fill in False, or the sample number (True and 1 are the same)
    return itertools, os, re, sample


@app.cell
def _(os, re, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # Problem-specific post-processing
        data = data.split("\n\n")
        output = {"rules": {v[0]:v[1].replace('"', '').split(" | ") \
                            for v in re.findall(r"(\d+):\s([\w\s|\"]+)[\n]", data[0]+"\n")}, \
                  "messages": data[1].strip().split("\n")}
        print(output)
        return output

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").read())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data, itertools, re):
    def substitute_rules(input_rules, max_iter=None):
        rules = input_rules.copy()
        # Keep replacing numbers until there are only a's and b's left
        i = 0
        while True and (max_iter is None or i < max_iter):
            i += 1
            # Go through all rules and replace numbers with rules with that key
            for k in rules.keys():
                new_rule = []
                # Loop through each piped (|) rule
                for rule in rules[k]:
                    # Get all piped combinations when replacing numbers with other rules
                    nr_combinations = [rules[n] if n.isdigit() else n for n in rule.split(" ")]
                    # Itertools.product takes all combinations such that [[1], [2, 3], [4]] becomes [1 2 4, 1 3 4]
                    new_rule += [' '.join(i) for i in list(itertools.product(*nr_combinations))]
                rules[k] = new_rule
            # Break if all numbers are replaced with letters
            if not len(re.findall(r'\d+', ' '.join([' '.join(r) for r in rules.values()]))):
                break
        return rules


    def problem_a(data):
        rules = substitute_rules(data["rules"])
        zero_rules = [r0.replace(" ", "") for r0 in rules["0"]]
        num_compliant = sum([1 for m in data["messages"] if m in zero_rules])

        return num_compliant
    answer_a = problem_a(input_data)
    return answer_a, substitute_rules


@app.cell
def _(input_data, substitute_rules):
    def problem_b(data):
        # # DON'T RUN - SERVER WILL CRASH
        # # Update rules as described to 8: 42 | 42 8, and 11: 42 31 | 42 11 31
        # rules = data["rules"].copy()
        # rules["8"] = ["42", "42 8"]
        # rules["11"] = ["42 31", "42 11 31"]
        # rules = substitute_rules(rules, max_iter=10)
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
