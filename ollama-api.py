import ollama
import clingo
import os

import llm_constants
import asp_constants

prompt = 'Name an engineer that passes the vibe check'

# ----------------------------------------------------------------------
# - Function Definitoins -----------------------------------------------
# ----------------------------------------------------------------------
def queryLLM(prompt="", model="llama3", show_stream=False):
    # if len(prompt) == 0:
    #     print("Please set a Prompt, default is empty!")
    #     return ""
    # try:
    # else:
	response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}], stream=show_stream)
	return response

    # except Exception as e:
    # 	return f"An error occurred: {e}"


def makePrompt(nl_answerset, nl_observations):
    final_prompt = ""

    final_prompt += llm_constants.PREPROMPT_2

    final_prompt += llm_constants.PLAN_PREPROMT
    for item in nl_answerset:
        final_prompt += (item + "\n")
    
    final_prompt += "\n"

    final_prompt += llm_constants.OBSERVATION_PREPROMT
    for item in nl_observations:
        final_prompt += (item + "\n")

    final_prompt += "\n"

    final_prompt += llm_constants.START_LOCATION
    final_prompt += llm_constants.ADJACENT_LOCATIONS

    final_prompt += llm_constants.FIRST_QUERY

    return final_prompt

def translator(item, interpretation_rules):
    relation, rest = item.split('(', 1)
    args = rest.rstrip(')').split(',')
    return interpretation_rules[relation](*args)

def translateAnswerSet(answer_set, interpretation_rules, num_of_set=0):  
    interpreted_strings = [translator(item, interpretation_rules) for item in answer_set[num_of_set]]
    return interpreted_strings

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
    else:
        print("Unsatisfiable")
    

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
    

# ----------------------------------------------------------------------
# - Main ---------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    
    ASP_FILE_PATH = "ASP.pl"

    # answer_sets_file = asp_constants.TEST_PLAN
    answer_sets_file = solveASP(ASP_FILE_PATH)
    printAnswerSet(answer_sets_file)

    # if len(answer_sets_file[0]) != 0: # only translate if an answerset is given
    #     translated_answerset = translateAnswerSet(answer_sets_file, asp_constants.INTERPRETER_RULES, 0)
        
    # else:
    #     print("No answerset to translate!")j

    # for item in llm_constants.TEST_OBSERVATION:
    #     print(item)
    # response = "\nNOTE: The LLM is currently not used, uncommend function call to acitvate it!\n"
    # response = queryLLM(prompt="Write a letter about flowers for my sister!", pre_prompt="") 
    # print(response)
    
    # final_prompt = makePrompt(translated_answerset, asp_constants.TEST_OBSERVATION)
    # response = queryLLM(final_prompt, show_stream=llm_constants.SHOW_STREAM)
    # for chunk in response:
    #     print(chunk['message']['content'], end='', flush=True)