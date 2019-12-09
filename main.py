from multiprocessing import freeze_support
from AttackDice import AttackDice
from DefenseDice import DefenseDice


def getInput(include_black=True):
    red = int(input("How many red dice? (0): ") or 0)
    if include_black:
        black = int(input("How many black dice? (0): ") or 0)
    else:
        black = 0
    white = int(input("How many white dice? (0): ") or 0)
    surge = input("Can the unit convert surges? (yes): ") or "true"
    surge = surge.lower() in ['true', '1', 'y', 'yes']
    rolls = int(input("How many times do you want to roll? (10000): ") or 10000)

    return {
        "red": red,
        "black": black,
        "white": white,
        "surge": surge,
        "rolls": rolls,
    }


if __name__ == '__main__':
    # import timeit

    freeze_support()

    mode = input("Attack or Defend? (attack): ").lower() or "attack"

    if mode == "defend":
        dice = DefenseDice()
        userInput = getInput(False)
        result = dice.test(userInput["red"], userInput["white"], userInput["rolls"], userInput["surge"])
    else:
        dice = AttackDice()
        userInput = getInput(True)
        result = dice.test(userInput["red"], userInput["black"], userInput["white"], userInput["rolls"], userInput["surge"])

    print("On the %s the roll is likely to have %s successes" % (mode, result))

    # elapsed_time = timeit.timeit("test()", number=1, setup="from __main__ import test")
    # print("Elapsed time %s" % elapsed_time)
