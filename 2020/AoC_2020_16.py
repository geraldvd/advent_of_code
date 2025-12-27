import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import re
    import math

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
    return math, os, re, sample


@app.cell
def _(os, re, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        rules, your_ticket, nearby_tickets = data.split("\n\n")
        data = {"rules": {}, "your_ticket": (), "nearby_tickets": []}
        for r in rules.split("\n"):
            res = re.findall(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", r)[0]
            data["rules"][res[0]] = (
                (int(res[1]), int(res[2])),
                (int(res[3]), int(res[4])),
            )
        data["your_ticket"] = tuple(
            [int(y) for y in your_ticket.split("\n")[1].split(",")]
        )
        for t in nearby_tickets.split("\n")[1:]:
            data["nearby_tickets"].append(tuple([int(y) for y in t.split(",")]))
        print(data)
        return data


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
def _(input_data):
    def sum_invalid_numbers(ticket, rules):
        """If sum of invalid numbers on ticket is >0, ticket is invalid"""
        invalid_numbers = []
        for num in ticket:
            num_valid = False
            for r in rules.values():
                for r2 in r:
                    if num in range(r2[0], r2[1] + 1):
                        num_valid = True
                        break
                if num_valid:
                    break
            if not num_valid:
                invalid_numbers.append(num)
        return sum(invalid_numbers)


    def problem_a(data):
        ticket_scanning_error_rate = 0
        for t in data["nearby_tickets"]:
            ticket_scanning_error_rate += sum_invalid_numbers(t, data["rules"])
        return ticket_scanning_error_rate


    answer_a = problem_a(input_data)
    return answer_a, sum_invalid_numbers


@app.cell
def _(input_data, math, sum_invalid_numbers):
    def check_rule(num, rule_key, data):
        r1, r2 = data["rules"][rule_key]
        return num in range(r1[0], r1[1] + 1) or num in range(r2[0], r2[1] + 1)


    def problem_b(data):
        # Starting point: assume all rules are valid for all digits
        possible_rule_seqs = {
            k: list(range(len(data["your_ticket"]))) for k in data["rules"].keys()
        }

        # Extract valid tickets
        valid_tickets = [
            t
            for t in data["nearby_tickets"]
            if not sum_invalid_numbers(t, data["rules"])
        ]

        # Get all valid ticket indices per rule
        for kr in possible_rule_seqs.keys():
            for t in valid_tickets:
                new_seq = set()
                for i in possible_rule_seqs[kr]:
                    if check_rule(t[i], kr, data):
                        new_seq.add(i)
                possible_rule_seqs[kr] = new_seq.copy()

        # Extract unique rule sequence (by exclusion)
        rule_per_number_index = {}
        for k in sorted(
            possible_rule_seqs.keys(), key=lambda x: len(possible_rule_seqs[x])
        ):
            for i in possible_rule_seqs[k]:
                if i not in rule_per_number_index.keys():
                    rule_per_number_index[i] = k

        # Calculate product of ticket numbers that correspond to rule related to "departure"
        indices_to_consider = []
        for idx, rule in rule_per_number_index.items():
            if "departure" in rule:
                indices_to_consider.append(idx)
        return math.prod([data["your_ticket"][i] for i in indices_to_consider])


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
