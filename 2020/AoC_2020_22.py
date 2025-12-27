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
        player1, player2 = data.strip().split("\n\n")
        player1 = [int(p) for p in player1.split("\n")[1:]]
        player2 = [int(p) for p in player2.split("\n")[1:]]
        print(f"Player 1: {player1}, Player 2: {player2}")
        return (player1, player2)


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
    def problem_a(data):
        player1 = data[0].copy()
        player2 = data[1].copy()
        while len(player1) and len(player2):
            c1 = player1.pop(0)
            c2 = player2.pop(0)
            if c1 > c2:
                player1.append(c1)
                player1.append(c2)
            elif c2 > c1:
                player2.append(c2)
                player2.append(c1)
            else:
                print("Note: cards were the same!")
                player1.append(c1)
                player2.append(c2)
        winning_player = player1 if len(player1) else player2
        return sum([(i + 1) * c for i, c in enumerate(winning_player[::-1])])


    answer_a = problem_a(input_data)
    return (answer_a,)


@app.cell
def _(input_data):
    def hand_hash(h):
        """Hash number for hands that should be unique for given order (assumption: numbers under 100)"""
        return sum([100**i * c for i, c in enumerate(h)])


    def recursive_combat(player1, player2):
        """Recursive function that plays recursive combat game.
        - input: player1 and player2 hands (list of numbers)
        - output: winning_player (1 or 2) and score.
        """
        p1 = player1.copy()
        p2 = player2.copy()
        history_p1 = []
        history_p2 = []

        # Before either player deals a card, if there was a previous round in this game that had exactly the same cards
        # in the same order in the same players' decks, the game instantly ends in a win for player 1.
        # Previous rounds from other games are not considered.
        # (This prevents infinite games of Recursive Combat, which everyone agrees is a bad idea.)
        if hand_hash(p1) in history_p1 or hand_hash(p2) in history_p2:
            # Player 1 wins the game
            return 1, sum([(i + 1) * c for i, c in enumerate(p1[::-1])])

        # Add current hands to history
        history_p1.append(hand_hash(p1))
        history_p2.append(hand_hash(p2))

        # Otherwise, players pick top card as normal
        counter = 0  # TODO: counter needed, because inner games still lock-up.
        while len(p1) and len(p2) and counter < 5000:
            counter += 1
            c1 = p1.pop(0)
            c2 = p2.pop(0)

            # If both players have at least as many cards remaining in their deck as the value of the card they just drew,
            # the winner of the round is determined by playing a new game of Recursive Combat.
            # Number of cards: number on the drawn card (a copy!)
            if len(p1) >= c1 and len(p2) >= c2:
                # Recursive combat!
                winning_player, _ = recursive_combat(p1[:c1], p2[:c2])

            # Otherwise, at least one player must not have enough cards left in their deck to recurse;
            # the winner of the round is the player with the higher-value card.
            else:
                if c1 > c2:
                    winning_player = 1
                elif c2 > c1:
                    winning_player = 2
                else:
                    assert False, "Error: should never happen"

            # Give cards to winning player in right order
            if winning_player == 1:
                p1.append(c1)
                p1.append(c2)
            elif winning_player == 2:
                p2.append(c2)
                p2.append(c1)
            else:
                assert False, "Error: should never happen"

        winning_player = 1 if len(p1) else 2
        return winning_player, sum(
            [(i + 1) * c for i, c in enumerate(eval(f"p{winning_player}")[::-1])]
        )


    def problem_b(data):
        winning_player, winning_score = recursive_combat(data[0], data[1])
        return winning_score


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
