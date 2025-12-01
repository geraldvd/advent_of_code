import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np

    # Settings
    sample = True # Fill in False, or the sample number (True and 1 are the same)
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
    def parse_direction_string(s):
        return s.replace('se', 'se,').replace('sw', 'sw,').replace('nw', 'nw,').replace('ne', 'ne,') \
                .replace('ws', 'w,s').replace('wn', 'w,n').replace('es', 'e,s').replace('en', 'e,n') \
                .replace('ee', 'e,e').replace('ww', 'w,w').replace('ew', 'e,w').replace('we', 'w,e') \
                .strip(',').split(',')

    def netto_move(moves):
        dir_count = {}
        for m in moves:
            for d in m:
                if d not in dir_count.keys():
                    dir_count[d] = 0
                dir_count[d] += 1
    
        # dir_count = {k:len([1 for m in moves if m == k]) for k in set(moves)}
        # pairs = [('se', 'nw'), ('sw', 'ne'), ('e', 'w')]
        pairs = [('n', 's'), ('e', 'w')]
        for p1, p2 in pairs:
            if p1 in dir_count.keys() and p2 in dir_count.keys():
                min_p1p2 = min(dir_count[p1], dir_count[p2])
                dir_count[p1] -= min_p1p2
                dir_count[p2] -= min_p1p2
                # if dir_count[p1] == 0:
                #     del dir_count[p1]
                # if dir_count[p2] == 0:
                #     del dir_count[p2]
        return ','.join([f"{k}:{v}" for k, v in sorted(dir_count.items(), key=lambda l: l[0])])
    

    def problem_a(data):
        tiles = {}
        for d in data:
            moves = parse_direction_string(d)
            # print(moves)
            nm = netto_move(moves)
            if nm not in tiles.keys():
                tiles[nm] = 0
            tiles[nm] += 1
        print(tiles)
        print([v for v in tiles.values()])
        return None
    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def problem_b(data):
        # TODO solve problem b
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
