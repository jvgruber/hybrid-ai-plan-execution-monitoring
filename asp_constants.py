INTERPRETER_RULES = {
    'move': lambda x: f"The agent moves to location {x} from the previous location.",
    'pickup': lambda x: f"The agent picks up package {x} at the current location.",
    'release': lambda x: f"The agent releases package {x} at the current location."
}

TEST_PLAN = [['move(B)', 'pickup(1)', 'move(C)', 'move(E)', 'release(1)', 'pickup(2)', 'move(C)', 'move(B)', 'release(2)']]

TEST_OBSERVATION = ["Package 1 is at location b", 'No package is at location c', 'Package 2 is at location e', 'No package is at location c', 'Package 1 is at location b']
