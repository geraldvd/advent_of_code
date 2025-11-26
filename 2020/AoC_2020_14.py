import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # Import statements
    import os
    import numpy as np
    import re

    # Settings
    sample = False # Fill in False, or the sample number (True and 1 are the same)
    return os, re, sample


@app.cell
def _(os, re, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        # Problem-specific post-processing
        processed_data = []
        for d in data.strip().split('mask = '):
            if d.strip() == '': 
                continue
            ds = d.split('\n')
            dd = {'mask': ds[0].strip(), 'mem': []}
            for dsi in ds[1:]:
                res = re.findall(r'\d+', dsi)
                if len(res):
                    dd['mem'].append((int(res[0]), int(res[1])))
            processed_data.append(dd)
        print(processed_data)
        return processed_data

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").read())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data):
    def bin2num(b):
        '''Convert binary string (excl. 0b in front) to an int'''
        return sum([int(bi)*2**(len(b)-i-1) for i, bi in enumerate(b)])

    def problem_a(data):
        mems = {}
        for d in data:
            # AND mask to overwrite zeros, OR mask to overwrite ones
            and_mask = bin2num(d['mask'].replace('X', '1'))
            or_mask = bin2num(d['mask'].replace('X', '0'))
            for m in d['mem']:
                mems[m[0]] = m[1] & and_mask | or_mask
        return sum(mems.values())
    answer_a = problem_a(input_data)
    return answer_a, bin2num


@app.cell
def _(bin2num, input_data):
    def address_mask(addr, mask):
        '''Apply the rules in the problem, returning a binary string with X still in there'''
        addr = bin(addr)[2:].zfill(len(mask))
        res = []
        for i, m in enumerate(mask):
            if m == '0':
                res.append(addr[i])
            elif m in ['1', 'X']:
                res.append(m)
            else:
                print('This should never happen.')
        return ''.join(res)

    def address_combinations(addr):
        '''Find all addresses to store the value in'''
        addr_list = []
        # Find all indices with 'X'
        x_idx = [addr.find('X')]
        while x_idx[-1] >= 0:
            search_res = addr[x_idx[-1]+1:].find('X')
            x_idx.append(search_res+x_idx[-1]+1 if search_res>=0 else search_res)

        # Get all combinations of X replaced by 0 and 1 and convert to int
        addr_list = [addr]
        for idx in x_idx[:-1]:
            new_addr_list = []
            for a in addr_list:
                new_addr_list.append(a[:idx]+'0'+a[idx+1:])
                new_addr_list.append(a[:idx]+'1'+a[idx+1:])
            addr_list = new_addr_list.copy()
        return [bin2num(a) for a in addr_list]


    def problem_b(data):
        mems = {}
        for d in data:
            for m in d['mem']:
                res_addr = address_mask(m[0], d['mask'])
                for a in address_combinations(res_addr):
                    mems[a] = m[1]
        return sum(mems.values())
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
