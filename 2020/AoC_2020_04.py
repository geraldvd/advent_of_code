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
def _(os, sample):
    # Get problem input
    day_number = os.path.basename(__file__).split(sep=".")[0].split(sep="_")[-1]
    def post_process(data):
        data = ''.join(data).strip().split('\n\n')
        passports = []
        for d in data:
            p = [p.split(':') for p in d.replace('\n', ' ').split(' ')]
            p = {k:v for k,v in p}
            passports.append(p)
        print(passports)
        return passports

    def load_input(sample=False):
        curdir = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/"
        filename = curdir + (f"input_{day_number}_sample{'_'+str(sample) if int(sample)>1 else ''}.txt" if sample else f"input_{day_number}.txt")
        return post_process(open(filename, "r").readlines())

    input_data = load_input(sample)
    return day_number, input_data


@app.cell
def _(input_data):
    def problem_a(data):
        # byr (Birth Year)
        # iyr (Issue Year)
        # eyr (Expiration Year)
        # hgt (Height)
        # hcl (Hair Color)
        # ecl (Eye Color)
        # pid (Passport ID)
        # cid (Country ID) - optional
        required_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
        valid_passports = 0
        for d in data:
            valid_passports += sum([r in d.keys() for r in required_keys]) == len(required_keys)
        return valid_passports
    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data, re):
    def problem_b(data):
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        # hgt (Height) - a number followed by either cm or in:
        #     If cm, the number must be at least 150 and at most 193.
        #     If in, the number must be at least 59 and at most 76.
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        # cid (Country ID) - ignored, missing or not.
        valid_passports = 0
        for d in data:
            byr = 'byr' in d.keys() and d['byr'].isdigit() and 1920 <= int(d['byr']) <= 2002
            iyr = 'iyr' in d.keys() and d['iyr'].isdigit() and 2010 <= int(d['iyr']) <= 2020
            eyr = 'eyr' in d.keys() and d['eyr'].isdigit() and 2020 <= int(d['eyr']) <= 2030
            hgt = 'hgt' in d.keys() and len(d['hgt']) > 2 and \
                ((d['hgt'][-2:] == 'cm' and d['hgt'][:-2].isdigit() and 150 <= int(d['hgt'][:-2]) <= 193) or \
                 (d['hgt'][-2:] == 'in' and d['hgt'][:-2].isdigit() and 59 <= int(d['hgt'][:-2]) <= 76))
            hcl = 'hcl' in d.keys() and re.search(r'^#[0-9a-f]{6}$', d['hcl']) is not None
            ecl = 'ecl' in d.keys() and d['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
            pid = 'pid' in d.keys() and re.search(r'^\d{9}$', d['pid']) is not None
            valid_passports += byr and iyr and eyr and hgt and hcl and ecl and pid
        return valid_passports
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
