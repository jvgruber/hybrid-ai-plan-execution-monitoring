import argparse

# Parse the asp output and extract the actions with their times
def parseASPOutput(output):
    actions = []
    for line in output.strip().split(' '):
        if line.startswith('execute'):
            # Extract the time and action
            time = int(line.split('(')[1].split(',')[0])
            action = line.split('(', 1)[1].rsplit(')', 1)[0].split(',', 1)[1]
            actions.append((time, action))
    return actions

# Sort the actions based on time
def sortActionsByTime(actions):
    sorted_actions = sorted(actions, key=lambda x: x[0])
    return [action for time, action in sorted_actions]

# Function to convert the ordered actions list to asp-style output
def actionsToASPOutput(actions_list):
    asp_statements = []
    for time, action in enumerate(actions_list):
        asp_statements.append(f"fault({time}) :- not execute({time},{action}).")
    return asp_statements

# Main function
def main():
    actions_list = ["move(d)", "move(f)", "load(three)", "move(d)", "release(three)", "move(e)", "load(two)", "move(c)", "wait"]
    asp_output = "execute(7,move(c)) execute(5,move(e)) execute(4,move(c)) execute(1,move(b)) execute(3,load(one)) execute(8,wait) execute(0,wait) execute(2,wait) execute(6,wait)"   

    parser = argparse.ArgumentParser(description="Translate between asp output and ordered actions.")
    parser.add_argument("mode", choices=["to_list", "to_asp", "sort_asp"], help="Mode of operation")
    args = parser.parse_args()

    if args.mode == "to_list":
        actions = parseASPOutput(asp_output)
        output_list = sortActionsByTime(actions)
        print(output_list)
    elif args.mode == "to_asp":
        asp_statements = actionsToASPOutput(actions_list)
        for statement in asp_statements:
            print(statement)
    elif args.mode == "sort_asp":
        actions = parseASPOutput(asp_output)
        actions_list = sortActionsByTime(actions)
        asp_statements = actionsToASPOutput(actions_list)
        for statement in asp_statements:
            print(statement)

if __name__ == "__main__":
    main()
