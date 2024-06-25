import llm_constants
import asp_constants

from asp_module import translateAnswerSet, printAnswerSet, solveASP
from llm_module import queryLLM, makePrompt, extractAnswer

if __name__ == "__main__":
    print("""
    ---------------------------------------------------------------
    Task 2:
    1. Query the LLM if a plan and the observations are consistent.
       - If Consistent -> Good
       - If Not -> Give the plan to ASP
         * generate automated ASP command and add it to pl-file.
         * THE AIM IS FIGURE OUT WHAT ACTIONS HAVE LET TO THE GIVEN OBSERVATIONS!
    2. Solve ASP programm
    ---------------------------------------------------------------\n
    """)
    
    # Constantx
    TIME_STEMPS = 8

    plan = [['start(0,a)','move(1,b)','pickup(2,1)','move(3,c)','release(4,1)','move(5,b)','move(6,a)']]
    falty_observation = [['packet_at(0,empty,a)','packet_at(1,one, b)','packet_at(3,empty,c)','packet_at(5,one,b)','packet_at(6,empty,a)']]
    correct_observation = [['packet_at(0,empty,a)','packet_at(1,one, b)','packet_at(3,empty,c)','packet_at(5,empty,b)','packet_at(6,empty,a)']]

    # -------------------------------------------------------------------
    # - 1. Translate the plan and the observartions to natural language -    
    # -------------------------------------------------------------------
    print("1. Translate the plan and the observartions to natural language\n")
    plan_tanslater = translateAnswerSet(plan, asp_constants.INTERPRETER_RULES_TASK_2)
    
    print("Plan:")
    for item in plan_tanslater:
        print(item)

    observation_translated = translateAnswerSet(falty_observation, asp_constants.INTERPRETER_RULES_TASK_2)

    print("Obs.:")
    for item in observation_translated:
        print(item)

    # -------------------------------------------------------------------
    # - 2. Generate a Prompt for the LLM --------------------------------
    # -------------------------------------------------------------------
    print("\n--------------------------------------------------------------------------------------------\n") 
    print("2. Generate a Prompt for the LLM\n")
    llm_query = "Can you please analyse the plan and the given observations step-by-step and check for inconsistencies."
    anwer_form = "If the plan and the observations are consistent, please wirte as last line **CONSISTENT**, if they are not wirte **INCONSISTENT**"

    prompt = makePrompt(preprompt=llm_constants.PREPROMPT_2,
                        plan_prepromtpt=llm_constants.PLAN_PREPROMT,
                        plan=plan_tanslater,
                        observation_prepropt=llm_constants.OBSERVATION_PREPROMT,
                        observaations=observation_translated,
                        adjacent_locations=llm_constants.ADJACENT_LOCATIONS,
                        query=llm_query,
                        answer_denotation=anwer_form
                        )

    print(prompt)


    # -------------------------------------------------------------------
    # - 3. Query LLM ----------------------------------------------------
    # -------------------------------------------------------------------
    print("\n--------------------------------------------------------------------------------------------\n") 

    response = queryLLM(prompt, show_stream=llm_constants.SHOW_STREAM) 

    if llm_constants.SHOW_STREAM:    
        for chunk in response:
            print(chunk['message']['content'], end='', flush=True)

    print(response)

    # -------------------------------------------------------------------
    # - 4. Extract Answer -----------------------------------------------
    # -------------------------------------------------------------------
    print("\n--------------------------------------------------------------------------------------------\n") 

    answer = extractAnswer(response)

    print(answer)
