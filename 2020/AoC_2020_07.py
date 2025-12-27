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
        data = [
            [
                i.replace(" no other", "")
                .replace(" bags", "")
                .replace(" bag", "")
                .replace(".", "")
                .strip()
                for i in d.split("contain")
            ]
            for d in data
        ]
        data = {k: v.split(", ") for k, v in data}
        data = {
            k: [(" ".join(v.split(" ")[1:]), v.split(" ")[0]) for v in data[k]]
            for k in data.keys()
        }
        # Make lists with empty strings empty
        for k in data.keys():
            if data[k] == [("", "")]:
                data[k] = []
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
    def problem_a(data):
        # Final bags are all parent bags that are valid
        final_bags = set()
        # List of bags that are not yet iterated
        next_bags = ["shiny gold"]
        while len(next_bags):
            checking_bag = next_bags.pop()
            for k, v in data.items():
                # Check if bag is in outer bag k, and if so: add it to next and final
                bags = [vi[0] for vi in v]
                if checking_bag in bags:
                    next_bags.append(k)
                    final_bags.add(k)
        return len(final_bags)


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def recurse_bag(data, bag="shiny gold", score=1):
        """Loop recursively through bags until a bag is empty, then add all scores"""
        # print(bag, score)
        end_score = score
        for inner_bag in data[bag]:
            end_score += recurse_bag(data, inner_bag[0], score * int(inner_bag[1]))
        return end_score


    def problem_b(data):
        # Deduct 1, to adjust for the initial score of 1 when calling recurse_bag
        score = recurse_bag(data) - 1
        return score


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
