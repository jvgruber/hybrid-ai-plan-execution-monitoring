import llm_constants
import asp_constants

from asp_module import translateAnswerSet, printAnswerSet
from llm_module import queryLLM, makePrompt

if __name__ == "__main__":
    print("""
    ---------------------------------------------------------------
    Task 1:
    1. Translate a given ASP plan to natural language, as well as the observations
    2. Query the LLM if plan and observations are consistent
       - If Consistent -> Good
       - If Not -> Use LLM to figure out what went wrong (which action failed)
    ---------------------------------------------------------------
    """)

    # TODO: Query LLM so that one answer comes out
    # TODO: Interprete the answer of LLM

    answer_sets_file = asp_constants.TEST_PLAN

    printAnswerSet(answer_sets_file)

    if len(answer_sets_file[0]) != 0: # only translate if an answerset is given
        translated_answerset = translateAnswerSet(answer_sets_file, asp_constants.INTERPRETER_RULES_TASK_1, 0)

        for item in translated_answerset:
            print(item)

    else:
        print("No answerset to translate!")

    for item in asp_constants.TEST_OBSERVATION:
        print(item)

    print("\n--------------------------------------------------------------------------------------------\n") 


    final_prompt = makePrompt(
                    llm_constants.PREPROMPT_3,
                    llm_constants.PLAN_PREPROMT, 
                    translated_answerset, 
                    llm_constants.OBSERVATION_PREPROMT,
                    asp_constants.TEST_OBSERVATION, 
                    llm_constants.FAULTS_AND_CAUSES, 
                    llm_constants.START_LOCATION, 
                    llm_constants.ADJACENT_LOCATIONS,
                    llm_constants.FIRST_QUERY + llm_constants.OUTPUT
                    )   
    
    print(final_prompt)
    print("\n--------------------------------------------------------------------------------------------\n") 
    response = queryLLM(final_prompt, show_stream=True)


    for chunk in response:
        print(chunk['message']['content'], end='', flush=True)