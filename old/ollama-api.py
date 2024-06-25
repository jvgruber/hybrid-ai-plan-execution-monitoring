import ollama
# import clingo
# import os

import llm_constants
import asp_constants

from asp_module import translator, translateAnswerSet, printAnswerSet, solveASP
from llm_module import queryLLM, makePrompt


if __name__ == "__main__":
    
    # ASP_FILE_PATH = "ASP.pl"

    # answer_sets_file = asp_constants.TEST_PLAN
    # answer_sets_file = solveASP(ASP_FILE_PATH)
    # printAnswerSet(answer_sets_file)

    # if len(answer_sets_file[0]) != 0: # only translate if an answerset is given
    #     translated_answerset = translateAnswerSet(answer_sets_file, asp_constants.INTERPRETER_RULES, 0)
        
    # else:
    #     print("No answerset to translate!")

    # for item in llm_constants.TEST_OBSERVATION:
    #     print(item)
    # response = "\nNOTE: The LLM is currently not used, uncommend function call to acitvate it!\n"
    # response = queryLLM(prompt="Write a letter about flowers for my sister!", pre_prompt="") 
    # print(response)
    
    # final_prompt = makePrompt(
    #                 llm_constants.PREPROMPT_3,
    #                 llm_constants.PLAN_PREPROMT, 
    #                 translated_answerset, 
    #                 llm_constants.OBSERVATION_PREPROMT,
    #                 asp_constants.TEST_OBSERVATION, 
    #                 llm_constants.FAULTS_AND_CAUSES, 
    #                 llm_constants.START_LOCATION, 
    #                 llm_constants.ADJACENT_LOCATIONS,
    #                 llm_constants.FIRST_QUERY + llm_constants.OUTPUT
    #                 )   

    final_prompt = makePrompt(llm_constants.TEST)

    print(final_prompt)
    print("\n--------------------------------------------------------------------------------------------\n") 
    response = queryLLM(final_prompt, show_stream=llm_constants.SHOW_STREAM)


    for chunk in response:
        print(chunk['message']['content'], end='', flush=True)