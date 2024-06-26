import os
import clingo

def translator(item, interpretation_rules):
    relation, rest = item.split('(', 1)
    
    if item[-1] == ".":
        args = rest.rstrip(').').split(',')
    else:
        args = rest.rstrip(')').split(',')
    
    args_sf = []
    for arg in args:
        args_sf.append(arg.strip())

    try:
        return interpretation_rules[relation](*args_sf)
    except Exception as e:
        print(f"Error: No translation rule is defined for the {e} predicate.")
        quit()

def translateAnswerSet(answer_set, interpretation_rules, num_of_set=0):  
    interpreted_strings = [translator(item, interpretation_rules) for item in answer_set[num_of_set]]
    return interpreted_strings

def printAnswerSet(answer_sets):
    """
    Takes in the anser sets form the solfeASP(...) functions an wirtes them to the console. The index is the number of the answer set.
    Which can be used in e.g. the translateAnswerSet(...) function to translate the answerset to natural language.
    """
    if answer_sets:
        print("SATISFIABLE")

        for i, answer_set in enumerate(answer_sets): 
            print(f"Answer Set {i}:\n {answer_set}")
    else:
        print("UNSATISFIABLE")
    

def solveASP(file_path, add_to_top = [""], tmin = -1):
    """
    This function takes in an ansolute or relativ path to a .pl file with and answer set program. This programm will be read and solved using clingo.
    Retuns a list of lists with the answer sets.
    """
    absolute_path = os.path.abspath(file_path)

    # Check if the file exists
    if not os.path.exists(absolute_path):
        raise FileNotFoundError(f"The file at {absolute_path} does not exist.")
        
    with open(file_path, 'r') as file:
        asp_program = file.read()
    
    ctl = clingo.Control()
    for item in add_to_top:
        ctl.add("base", [], item)
    
    if tmin != -1:
        ctl.add("base", [], f"#const max_time = {tmin}.")
    ctl.add("base", [], asp_program)
    ctl.ground([("base", [])])

    result = ctl.solve()

    answer_sets = []
    if result.satisfiable:
        for model in ctl.solve(yield_=True):
            answer_set = [str(atom) for atom in model.symbols(shown=True)]
            answer_sets.append(answer_set)

    return answer_sets