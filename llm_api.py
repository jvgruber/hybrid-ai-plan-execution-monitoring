import os
import clingo
import replicate

REPLICATE_API_TOKEN = "r8_FhBHx8c9jyv0xfY2bv1TGtMX5vK4eHb2tSAdv"
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# ----------------------------------------------------------------------
# - Function Definitoins -----------------------------------------------
# ----------------------------------------------------------------------
def queryLLM(prompt="", pre_prompt="", temperature=0.75,top_p=1.00, max_length=1023, repetition_penalty=1):
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
                "max_length": max_length,
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
    if answer_sets:
        print("Satisfiable")
        print("Answer Sets:")

        for i, answer_set in enumerate(answer_sets):
            print(f"Answer Set {i + 1}: {answer_set}")
    else:
        print("Unsatisfiable")

# ----------------------------------------------------------------------
# - Main ---------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    aps_file_path = "ASP.pl"

    answer_sets_file = solveASP(aps_file_path)
    printAnswerSet(answer_sets_file)

    response = "\nNOTE: The LLM is currently not used, uncommend function call to acitvate it!\n"
    # response = queryLLM(prompt="Write a letter about flowers for my sister!", pre_prompt="") 
    print(response)
    