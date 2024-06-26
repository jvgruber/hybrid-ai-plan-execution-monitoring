INTERPRETER_RULES_TASK_1 = {
    'move': lambda x: f"The robot moves to location {x} from the previous location.",
    'pickup': lambda x: f"The robot picks up package {x} at the current location.",
    'release': lambda x: f"The robot releases package {x} at the current location."
}

INTERPRETER_RULES_TASK_2 = {
    'start': lambda x, y: f"At time stemp {x} the robot starts at location {y}.",
    'move': lambda x, y: f"At time stemp {x} it moves to location {y} from current location.",
    'pickup': lambda x, y: f"At time stemp {x}  robot picksup package {y} at current location.",
    'release': lambda x, y: f"At time stemp {x}  robot releases the package {y} at current location.",
    'packet_at': lambda x, y, z : f"At time stemp {x} there is no package at location {z} " if y == "empty" else f"At time step {x} there package {y} is at locatin {z}."
}

TEST_PLAN = [['move(B)', 'pickup(1)', 'move(C)', 'move(E)', 'release(1)', 'pickup(2)', 'move(C)', 'move(B)', 'release(2)']]

TEST_OBSERVATION = ["Package 1 is at location b", 'No package is at location c', 'Package 2 is at location e', 'No package is at location c', 'Package 1 is at location b']

# deliver 3 to D, deliver 2 to C
TMIN_2 = 8
PLAN_2 = [['move(d)', 'move(f)', 'load(three)', 'move(d)', 'release(three)', 'move(e)', 'load(two)', 'move(c)', 'release(two)']]
OBSERVATION_2F = [['']]
OBSERVATION_2C = [["Package 1 is at location b"]]