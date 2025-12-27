import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import itertools

    # Settings
    sample = False  # Fill in False, or the sample number (True and 1 are the same)
    return os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        food = []  # List of tuples of list: [(ingredients=[], allergens=[]), ...]
        for d in data:
            ingredients, allergens = d.strip().strip(")").split(" (contains ")
            food_dict = {
                "ingredients": ingredients.split(" "),
                "allergens": allergens.split(", "),
            }
            food.append((ingredients.split(" "), allergens.split(", ")))
        print(food)
        return food


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
    def calculate_allergen_ingredients(data):
        """Return dict with allergen as key and the matching ingredient as value."""
        # First determine all possible ingredient options per allergen
        allergen_options = {}
        for ingredients, allergens in data:
            for a in allergens:
                if a not in allergen_options.keys():
                    allergen_options[a] = ingredients
                else:
                    allergen_options[a] = [
                        i for i in allergen_options[a] if i in ingredients
                    ]

        # Go through the allergen_options and find the 1:1 match with the right ingredients
        allergens_confirmed = {}
        while len(allergens_confirmed.keys()) != len(allergen_options.keys()):
            for allergen, ingredients in allergen_options.items():
                i_new = [
                    i for i in ingredients if i not in allergens_confirmed.values()
                ]
                if len(i_new) == 1:
                    allergens_confirmed[allergen] = i_new[0]

        return allergens_confirmed


    def problem_a(data):
        allergen_ingredients = calculate_allergen_ingredients(data)

        # Count total occurences of ingredients that don't have allergens
        counter = 0
        for ingredients, _ in data:
            for i in ingredients:
                if i not in allergen_ingredients.values():
                    counter += 1
        return counter


    answer_a = problem_a(input_data)
    return answer_a, calculate_allergen_ingredients


@app.cell
def _(calculate_allergen_ingredients, input_data):
    def problem_b(data):
        allergen_ingredients = calculate_allergen_ingredients(data)
        # Sort by allergen and return comma list of the matching ingredients
        return ",".join(
            [
                i[1]
                for i in sorted(allergen_ingredients.items(), key=lambda l: l[0])
            ]
        )


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
