import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import re
    import itertools

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
    return itertools, os, re, sample


@app.cell
def _(os, re, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        data = data.split("\n\n")
        output = {
            "rules": {
                v[0]: v[1].replace('"', "").split(" | ")
                for v in re.findall(r"(\d+):\s([\w\s|\"]+)[\n]", data[0] + "\n")
            },
            "messages": data[1].strip().split("\n"),
        }
        print(output)
        return output


    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (
            f"input_{day_number}_sample{'_' + str(sample) if int(sample) > 1 else ''}.txt"
            if sample
            else f"input_{day_number}.txt"
        )
        return post_process(open(filename, "r").read())


    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data, itertools, re):
    def substitute_rules(input_rules, max_iter=None):
        """Return dict of numbered rules, with a list of string sequences of a's and b's (with space in beteen).
        Method is iterative replacing of numbers by the matching rule strings."""
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
                    nr_combinations = [
                        rules[n] if n.isdigit() else n for n in rule.split(" ")
                    ]
                    # Itertools.product takes all combinations such that [[1], [2, 3], [4]] becomes [1 2 4, 1 3 4]
                    new_rule += [
                        " ".join(i)
                        for i in list(itertools.product(*nr_combinations))
                    ]
                rules[k] = new_rule
            # Break if all numbers are replaced with letters
            if not len(
                re.findall(r"\d+", " ".join([" ".join(r) for r in rules.values()]))
            ):
                break
        return rules


    # Calculate rules once, since it takes longest to calculate
    rules = substitute_rules(input_data["rules"])
    return (rules,)


@app.cell
def _(input_data, rules):
    def problem_a(data):
        zero_rules = [r0.replace(" ", "") for r0 in rules["0"]]
        num_compliant = sum([1 for m in data["messages"] if m in zero_rules])

        return num_compliant


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data, rules):
    def problem_b(data):
        """General/iterative solution too complicated. Based on hint in question ("it might help to start by looking
        at which rules always match the same set of values and how those rules (especially rules 42 and 31)")
        it's better to work out rules 0 in more detail

        Original rules:
        0: 8 11 = 42 42 31
        8: 42
        11: 42 31

        New rules:
        0: 8 11 = 42 (...) 42 [42 (...) 31] 31 = 42 (*X) 31 (*Y) --> I.e., it's always a sequence of 42's and 31's.
        8: 42 | 42 8
        11: 42 31 | 42 11 31

        Options rule 0 with different loops show that
            1) first and second parts are ALWAYS rule 42,
            2) last part is ALWAYS rule 31, and
            3) count of rule 42 > count rule 31.
        42 42 31 (no loop)
        42 42 42 31 (1x loop 8)
        42 42 42 31 31 (1x loop 11)
        42 42 42 42 31 31 31 (2x loop 11)
        """
        # Extract list of sequences showing rules 31 and 42 (the relevant ones)
        rule31 = [r.replace(" ", "") for r in rules["31"]]
        rule42 = [r.replace(" ", "") for r in rules["42"]]
        # Visually observed: parts are always same length, just checking here and assigning rule_length
        assert min([len(s) for s in rule31 + rule42]) == max(
            [len(s) for s in rule31 + rule42]
        ), "Expected same length for all rules."
        rule_length = len(rule31[0])

        # Loop through messages and check on rules and conditions in function header.
        num_compliant = 0
        for m in data["messages"]:
            # Make sure once switched from rule 42 to 31, there is no way back.
            switched_to_31 = False
            # Counters to check num_42 > num_31
            num_42 = 0
            num_31 = 0
            # Check conditions: always multiple of rule_length, and at least 2x rule 42 and 1x rule 31.
            if (
                len(m) % rule_length == 0
                and m[:rule_length] in rule42
                and m[rule_length : 2 * rule_length] in rule42
                and m[-rule_length:] in rule31
            ):
                # Go through sections of "rule_length" length, and confirm rules are followed
                compliant = True
                for i in range(0, len(m), rule_length):
                    if not switched_to_31 and m[i : i + rule_length] in rule42:
                        num_42 += 1
                        continue
                    elif m[i : i + rule_length] in rule31:
                        num_31 += 1
                        switched_to_31 = True
                        continue
                    else:
                        compliant = False
                        break
                if compliant and num_42 > num_31:
                    num_compliant += 1
        return num_compliant


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
