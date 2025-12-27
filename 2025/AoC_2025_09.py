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
    return np, os, sample


@app.cell
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]


    def post_process(data):
        # Problem-specific post-processing
        data = [tuple([int(i) for i in d.strip().split(",")]) for d in data]
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
def _(input_data, np):
    def area_matrix(data):
        """Create a numpy matrix with rows and columns the indices of list data and values the area of that rectangle."""
        # Calculate all possible rectangle areas in a matrix
        areas = np.ones((len(data), len(data)))
        for i1, c1 in enumerate(data):
            for i2, c2 in enumerate(data):
                areas[i1, i2] = (abs(c2[0] - c1[0]) + 1) * (abs(c2[1] - c1[1]) + 1)
        return areas


    def problem_a(data):
        # Calculate all possible rectangle areas in a matrix
        areas = area_matrix(data)
        # Return maximum area found
        return int(areas.max())


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def area_list(data):
        """Return sorted list (by area) of areas in form: tuple((coord1 idx in data, coord2 idx in data), area)"""
        areas = []
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                areas.append(
                    (
                        (i, j),
                        (abs(data[i][0] - data[j][0]) + 1)
                        * (abs(data[i][1] - data[j][1]) + 1),
                    )
                )
        return sorted(areas, key=lambda x: x[1], reverse=True)


    def problem_b(data):
        # Get sorted list of all rectangles with area
        areas = area_list(data)

        # Loop through all rectanges and eliminate ones that are not fully enclosed.
        # First one to not be eliminated is the answer (since the list is sorted by area).
        for a in areas:
            # Extract indices and area for easy reference. Also, convert idx[2] to coordinates (c)
            idx, area = a
            c0, c1 = data[idx[0]], data[idx[1]]
            # Assumption: rectangle is valid until eliminated
            valid = True
            # Check 1: if there is a red tile enclosed by rectange --> Eliminate
            for d in data:
                if d[0] in range(min(c0[0], c1[0]) + 1, max(c0[0], c1[0])) and d[
                    1
                ] in range(min(c0[1], c1[1]) + 1, max(c0[1], c1[1])):
                    # Red tile in enclosed rectange, eliminate.
                    valid = False
                    break

            # Check 2: check that none of the line pieces of the perimiter are fully outside the rectangle
            # Walk the entire perimeter
            for i, d in enumerate(data):
                # Define two coordinates of adjacent red tiles
                r0, r1 = data[i - 1], data[i]
                # Vertical edge piece
                if r0[0] == r1[0]:
                    # Check: entirely left of rectangle OR entirely right OR entirely above OR entirely above
                    if not (
                        r0[0] <= min(c0[0], c1[0])
                        or r0[0] >= max(c0[0], c1[0])
                        or (
                            r0[1] <= min(c0[1], c1[1])
                            and r1[1] <= min(c0[1], c1[1])
                        )
                        or (
                            r0[1] >= max(c0[1], c1[1])
                            and r1[1] >= max(c0[1], c1[1])
                        )
                    ):
                        valid = False
                        break
                # Horizontal edge piece
                elif r0[1] == r1[1]:
                    # Check: entirely below of rectangle OR entirely above OR entirely left OR entirely right
                    if not (
                        r0[1] <= min(c0[1], c1[1])
                        or r0[1] >= max(c0[1], c1[1])
                        or (
                            r0[0] <= min(c0[0], c1[0])
                            and r1[0] <= min(c0[0], c1[0])
                        )
                        or (
                            r0[0] >= max(c0[0], c1[0])
                            and r1[0] >= max(c0[0], c1[0])
                        )
                    ):
                        valid = False
                        break
                else:
                    print("Error: this should never happen.")

            # Not eliminted means this is the maximum area found --> Answer
            if valid:
                return area


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
