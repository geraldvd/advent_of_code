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
        data = [int(i) for i in data.strip()]
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
    def move(cups):
        """
        The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
        The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
        The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
        The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        """
        # The crab picks up the three cups that are immediately clockwise of the current cup.
        # They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
        pick_ups = cups[1:4]
        # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
        # If this would select one of the cups that was just picked up, the crab will keep subtracting one until
        # it finds a cup that wasn't just picked up. If at any point in this process the value goes below the
        # lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
        destination = cups[0] - 1
        while destination in pick_ups or destination < min(cups):
            if destination < min(cups):
                destination = max(cups)
            else:
                destination -= 1
        dest_idx = cups.index(destination)
        # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
        # They keep the same order as when they were picked up.
        # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        # Note: current cup is always placed at the front (unlike the example)
        return cups[4 : dest_idx + 1] + pick_ups + cups[dest_idx + 1 :] + cups[:1]


    def problem_a(data):
        cups = data.copy()
        print(cups)
        for i in range(100):
            cups = move(cups)
            print(cups)
        # Resequence such that the cup after 1 comes first, and does not include 1 at the end
        return "".join(
            [str(i) for i in cups[cups.index(1) + 1 :] + cups[: cups.index(1)]]
        )


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _():
    class Node:
        """Linked list node, keeping track of pointers to next and prev element."""

        def __init__(self, val, prev=None, next=None):
            self.value = val
            self.prev = prev
            self.next = next

        def __repr__(self):
            return f"Node {self.value}. Prev set: {self.prev is not None}, Next set: {self.next is not None}."


    class Cups:
        """Linked list implementation is efficient, since it does not require moving around elements in lists.
        For the move function (which is called 10M times), it only requires simple assignment of a few next/prev pointers."""

        def __init__(self, initial_values: list[int]):
            # Initialize double linked list
            self.cups = []
            prev = None
            next = None
            for v in initial_values:
                n = Node(v, prev, next)
                self.cups.append(n)
                prev = n
            # Loop around: prev node of first item is the last one
            self.cups[0].prev = self.cups[-1]
            # Set the next values of each node
            for i in range(len(self.cups)):
                if i < len(self.cups) - 1:
                    self.cups[i].next = self.cups[i + 1]
                else:
                    # Loop around: next node of last item is the first node
                    self.cups[i].next = self.cups[0]

            # Create value hash map (for efficient destination finding), cur_cup start value and min and max of list
            self.cup_values = {c.value: c for c in self.cups}
            self.cur_cup = self.cups[0]
            self.max_value = max([c.value for c in self.cups])
            self.min_value = min([c.value for c in self.cups])

        def __repr__(self):
            cups = [self.cur_cup]
            while cups[-1] is not self.cur_cup.prev:
                cups.append(cups[-1].next)
            return f"cups: {[c.value for c in cups]}, cur_cup: {self.cur_cup}"

        def move(self):
            """Do a single move, as described in the assignment. Note that problem a can also be solved with this implementation."""
            # The crab picks up the three cups that are immediately clockwise of the current cup.
            # They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
            pick_ups = [
                self.cur_cup.next,
                self.cur_cup.next.next,
                self.cur_cup.next.next.next,
            ]
            self.cur_cup.next = pick_ups[-1].next
            pick_ups[-1].next.prev = self.cur_cup
            pick_ups[0].prev = None
            pick_ups[-1].next = None

            # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
            # If this would select one of the cups that was just picked up, the crab will keep subtracting one until
            # it finds a cup that wasn't just picked up. If at any point in this process the value goes below the
            # lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
            dest_value = self.cur_cup.value - 1
            pick_up_values = [p.value for p in pick_ups]
            while dest_value in pick_up_values or dest_value < self.min_value:
                if dest_value < self.min_value:
                    dest_value = self.max_value
                else:
                    dest_value -= 1
            # dest = [c for c in self.cups if c.value == dest_value]
            # assert len(dest) == 1, "Destination should only have one element"
            # dest = dest[0]
            dest = self.cup_values[dest_value]

            # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
            # They keep the same order as when they were picked up.
            pick_ups[0].prev = dest
            pick_ups[-1].next = dest.next
            dest.next.prev = pick_ups[-1]
            dest.next = pick_ups[0]

            # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
            self.cur_cup = self.cur_cup.next
    return (Cups,)


@app.cell
def _(Cups, input_data):
    def problem_b(data):
        # Initial values is a list of a million values, starting with data.
        # Note: this assumes data contains all numbers in [1, len(data)]
        initial_values = data.copy() + list(range(1, 1_000_001))[len(data) :]
        cups = Cups(initial_values)
        for i in range(10_000_000):
            cups.move()
        # Return product of the two values next to the cup with value 1.
        return cups.cup_values[1].next.value * cups.cup_values[1].next.next.value


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
