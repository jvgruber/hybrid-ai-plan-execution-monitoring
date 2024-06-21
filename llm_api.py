import os
import clingo
import replicate

import llm_constants

REPLICATE_API_TOKEN = "r8_6cYYhhQxEK7CuFzLDx061KjxL0hNWVg3aQGcl"
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# ----------------------------------------------------------------------
# - Function Definitoins -----------------------------------------------
# ----------------------------------------------------------------------
def queryLLM(prompt="", pre_prompt="", temperature=0.75,top_p=1.00, max_new_tokens=500, repetition_penalty=1):
    if len(prompt) == 0:
        print("Please set a Promt, default is empty!")
        return ""
    try:
        output = replicate.run(
            "meta/llama-2-13b-chat",
            input={
                "prompt": f"{pre_prompt} {prompt}",
                "temperature": temperature,
                "top_p": top_p,
                "max_new_tokens": max_new_tokens,
                "repetition_penalty": repetition_penalty
            }
        )

        full_response = ""
        for item in output:
            full_response += item

        return full_response

    except Exception as e:
        return f"An error occurred: {e}"
    

def solveASP(file_path):
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
    ctl.add("base", [], asp_program)
    ctl.ground([("base", [])])

    result = ctl.solve()

    answer_sets = []
    if result.satisfiable:
        for model in ctl.solve(yield_=True):
            answer_set = [str(atom) for atom in model.symbols(shown=True)]
            answer_sets.append(answer_set)

    return answer_sets
  

def printAnswerSet(answer_sets):
    """
    Takes in the anser sets form the solfeASP(...) functions an wirtes them to the console. The index is the number of the answer set.
    Which can be used in e.g. the translateAnswerSet(...) function to translate the answerset to natural language.
    """
    if answer_sets:
        print("Satisfiable")
        print("Answer Sets:")

        for i, answer_set in enumerate(answer_sets):
            print(f"Answer Set {i}: {answer_set}")
        return True
    else:
        print("Unsatisfiable")
        return False


def traslator(item, interpretation_rules):
    relation, rest = item.split('(', 1)
    args = rest.rstrip(')').split(',')
    return interpretation_rules[relation](*args)


def translateAnswerSet(answer_set, interpretation_rules, num_of_set=0):  
    interpreted_strings = [traslator(item, interpretation_rules) for item in answer_set[num_of_set]]
    return interpreted_strings


# ----------------------------------------------------------------------
# - Main ---------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    ASP_FILE_PATH = "ASP.pl"

    answer_sets_file = solveASP(ASP_FILE_PATH)
    answer_sets_file = [['move(B)', 'pickup(1)', 'move(C)', 'move(E)', 'release(1)', 'pickup(2)', 'move(C)', 'move(B)', 'release(2)']]

    has_answerset = printAnswerSet(answer_sets_file)

    if len(answer_sets_file[0]) != 0: # only translate if an answerset is given
        translated_answerset = translateAnswerSet(answer_sets_file, llm_constants.INTERPRETER_RULES, 0)
        print(translated_answerset)
    else:
        print("No answerset to translate!")



    # response = "\nNOTE: The LLM is currently not used, uncommend function call to acitvate it!\n"
    # response = queryLLM(prompt="Write a letter about flowers for my sister!", pre_prompt="") 
    # print(response)
    
    pre_prompt = ""