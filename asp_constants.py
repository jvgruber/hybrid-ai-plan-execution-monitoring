INTERPRETER_RULES_TASK_1 = {
    'move': lambda x: f"The robot moves to location {x} from the previous location.",
    'load': lambda x: f"The robot picks up package {x} at the current location.",
    'release': lambda x: f"The robot releases package {x} at the current location."
}

INTERPRETER_RULES_TASK_2 = {
    'robot_at': lambda x: f"The robot starts at location {x}.",
    'move': lambda x: f"At time stemp * it moves to location {x} from current location.",
    'load': lambda x: f"At time stemp * robot picksup package {x} at current location.",
    'release': lambda x: f"At time stemp * robot releases the package {x} at current location.",
    'packet_at': lambda x, y, z : f"At time stemp {x} there is no package at location {z} " if y == "empty" else f"At time step {x} there package {y} is at locatin {z}.",
    'saw_packet_at': lambda x, y :f"Robot observed package {y} at time stemp {x}",
    ':- saw_packet_at': lambda x, y : f"Robot did not see a package at time stemp {x}"
}

# assignment example plan
TMIN_1 = 9
PLAN_1 = [['move(b)', 'load(one)','move(b)', 'move(b)', 'release(one)', 'load(two)', 'move(c)', 'move(b)', 'release(two)']]
OBSERVATION_1C = [['saw_packet_at(1,one).',':- saw_packet_at(3,P).', 'saw_packet_at(4,two).', ':- saw_packet_at(7,P).', ':- saw_packet_at(8,P).']]
OBSERVATION_1F = [['saw_packet_at(1,one).',':- saw_packet_at(3,P).', 'saw_packet_at(4,two).', ':- saw_packet_at(7,P).', 'saw_packet_at(8,one).']]

# deliver 3 to D, deliver 2 to C - fault: move(b) instead of move(f)
TMIN_2 = 9
PLAN_2 = [['move(d)', 'move(f)', 'load(three)', 'move(d)', 'release(three)', 'move(e)', 'load(two)', 'move(c)', 'release(two)']]
OBSERVATION_2C = [[':- saw_packet_at(1, P).', 'saw_packet_at(2, three).', ':- saw_packet_at(4, P).', 'saw_packet_at(5, three).', 'saw_packet_at(6, two).', ':- saw_packet_at(8, P).']]
OBSERVATION_2F = [[':- saw_packet_at(1, P).', 'saw_packet_at(2, one).', ':- saw_packet_at(4, P).', 'saw_packet_at(5, one).', 'saw_packet_at(6, two).', ':- saw_packet_at(8, P).']]

# deliver 1 to F, deliver 3 to H, end at B - fault: fail at release(one)
TMIN_3 = 11
PLAN_3 = [['move(b)', 'load(one)', 'move(d)', 'release(one)', 'move(f)', 'load(three)', 'move(h)', 'release(three)', 'move(f)', 'move(d)', 'move(b)']]
OBSERVATION_3C = [['saw_packet_at(1, one).', ':- saw_packet_at(3, P).', 'saw_packet_at(5, three).', ':- saw_packet_at(7, P).', ':- saw_packet_at(9, P).', 'saw_packet_at(10, one).', ':- saw_packet_at(11, P).']]
OBSERVATION_3F = [['saw_packet_at(1, one).', ':- saw_packet_at(3, P).', 'saw_packet_at(5, three).', ':- saw_packet_at(7, P).', 'saw_packet_at(9, three).', ':- saw_packet_at(10, P).', ':- saw_packet_at(11, P).']]

# deliver 1 to F, deliver 3 to H, end at A - fault: fail at release(one) [harder than 3 bc A is empty anyways]
TMIN_4 = 11
PLAN_4 = [['move(b)', 'load(one)', 'move(d)', 'release(one)', 'move(f)', 'load(three)', 'move(h)', 'release(three)', 'move(f)', 'move(d)', 'move(a)']]
OBSERVATION_4C = [['saw_packet_at(1, one).', ':- saw_packet_at(3, P).', 'saw_packet_at(5, three).', ':- saw_packet_at(7, P).', ':- saw_packet_at(9, P).', 'saw_packet_at(10, one).', ':- saw_packet_at(11, P).']]
OBSERVATION_4F = [['saw_packet_at(1, one).', ':- saw_packet_at(3, P).', 'saw_packet_at(5, three).', ':- saw_packet_at(7, P).', 'saw_packet_at(9, three).', ':- saw_packet_at(10, P).', ':- saw_packet_at(11, P).']]

# deliver 1 to H, deliver 3 to D - fault: wumpus switched 2 and 3 [ASP rearranges most of the plan]
TMIN_5 = 10
PLAN_5 = [['move(b)', 'load(one)', 'move(d)', 'move(f)', 'move(h)', 'release(one)', 'move(f)', 'load(three)', 'move(d)', 'release(three)']]
OBSERVATION_5C = [['saw_packet_at(1, one).', ':- saw_packet_at(3, P).', 'saw_packet_at(4, three).', ':- saw_packet_at(5, P).', 'saw_packet_at(7, three).', ':- saw_packet_at(9, P).']]
OBSERVATION_5F = [['saw_packet_at(1, one).', ':- saw_packet_at(3, P).', 'saw_packet_at(4, two).', ':- saw_packet_at(5, P).', 'saw_packet_at(7, two).', ':- saw_packet_at(9, P).']]