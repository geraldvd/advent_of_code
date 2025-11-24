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
    return np, os, sample


@app.cell
def _(np, os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # Problem-specific post-processing
        data = np.array([list(d.strip()) for d in data])
        print(data)
        return data

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data, np):
    def data_to_coordinates(data):
        # Define initial floor squares, seat squares, full seats and empty seats
        floor_squares = set([tuple(i) for i in np.argwhere(data == '.')])
        empty_seats = set([tuple(i) for i in np.argwhere(data == 'L')])
        full_seats = set([tuple(i) for i in np.argwhere(data == '#')])
        seat_squares = empty_seats | full_seats
        return floor_squares, seat_squares, full_seats

    def apply_seating_rules_a(floor_squares, seat_squares, full_seats):
        new_full_seats = set()
        for s in seat_squares:
            # Compute adjacent seats
            adj_seats = [(s[0]+1, s[1]), (s[0]-1, s[1]), (s[0], s[1]+1), (s[0], s[1]-1), 
                         (s[0]+1, s[1]+1), (s[0]-1, s[1]-1), (s[0]+1, s[1]-1), (s[0]-1, s[1]+1)]
            adj_seats = set([a for a in adj_seats if a in seat_squares])
            # Rule 1: If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
            if s not in full_seats and not len([1 for a in adj_seats if a in full_seats]):
                new_full_seats.add(s)
            # Rule 2: If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
            elif s in full_seats and len([1 for a in adj_seats if a in full_seats]) >= 4:
                # Not added to full seats
                pass
            # Else: keep full seats full
            elif s in full_seats:
                new_full_seats.add(s)
        return new_full_seats

    def problem_a(data):
        floor_squares, seat_squares, full_seats = data_to_coordinates(data)

        # Iterate and calculate new full seats until it doesn't change anymore
        new_full_seats = apply_seating_rules_a(floor_squares, seat_squares, full_seats)
        while full_seats != new_full_seats:
            full_seats = new_full_seats.copy()
            new_full_seats = apply_seating_rules_a(floor_squares, seat_squares, full_seats)
        return len(full_seats)
    answer_a = problem_a(input_data)
    return answer_a, data_to_coordinates


@app.cell
def _(data_to_coordinates, input_data):
    def apply_seating_rules_b(floor_squares, seat_squares, full_seats, data):
        new_full_seats = set()
        for s in seat_squares:
            # Compute adjacent seats
            adj_seats = []
            for dx in [0, -1, 1]:
                for dy in [0, -1, 1]:
                    if not dx and not dy: 
                        continue
                    mult = 1
                    try_seat = (s[0]+mult*dy, s[1]+mult*dx)
                    while try_seat not in seat_squares:
                        if try_seat[0] >= data.shape[0] or try_seat[0] < 0 or \
                           try_seat[1] >= data.shape[1] or try_seat[1] < 0:
                            break
                        mult += 1
                        try_seat = (s[0]+mult*dy, s[1]+mult*dx)
                    if try_seat in seat_squares:
                        adj_seats.append(try_seat)
            # Rule 1: If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
            if s not in full_seats and not len([1 for a in adj_seats if a in full_seats]):
                new_full_seats.add(s)
            # Rule 2: If a seat is occupied (#) and five or more seats adjacent to it are also occupied, the seat becomes empty.
            elif s in full_seats and len([1 for a in adj_seats if a in full_seats]) >= 5:
                # Not added to full seats
                pass
            # Else: keep full seats full
            elif s in full_seats:
                new_full_seats.add(s)
        return new_full_seats

    def problem_b(data):
        floor_squares, seat_squares, full_seats = data_to_coordinates(data)
    
        # Iterate and calculate new full seats until it doesn't change anymore
        new_full_seats = apply_seating_rules_b(floor_squares, seat_squares, full_seats, data)
        while full_seats != new_full_seats:
            full_seats = new_full_seats.copy()
            new_full_seats = apply_seating_rules_b(floor_squares, seat_squares, full_seats, data)
        return len(full_seats)
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
