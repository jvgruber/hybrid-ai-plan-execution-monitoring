import llm_constants
import asp_constants
import time


from asp_module import translateAnswerSet, printAnswerSet
from llm_module import queryLLM, makePrompt, extractAnswer, extractFaultyActions

if __name__ == "__main__":
    print("""
    ---------------------------------------------------------------
    Task 1:
    1. Translate plan and observations to natural language
    2. Build prompt out of logical domain restrictions, plan, observations and query
    3. Query the LLM if plan and observations are consistent
    4. Read in the LLM response
    Note: The LLM should be used to find the error root cause
    ---------------------------------------------------------------
    """)

    time_start = time.time()

    print("""
    ---------------------------------------------------------------
    - 1. Translate the plan and observations to natural language -    
    ---------------------------------------------------------------
    """)

    # asp_constants.PLAN_n and asp_constants.OBSERVATIONS_nC/F denote which plan and which observation is used.
    # the observations can either be Consistent of Faulty
    PLAN = asp_constants.PLAN_1
    OBS = asp_constants.OBSERVATION_1C

    translated_plan = translateAnswerSet(PLAN, asp_constants.INTERPRETER_RULES_TASK_2, 0)
    translated_obs = translateAnswerSet(OBS, asp_constants.INTERPRETER_RULES_TASK_2, 0)

    print(translated_plan, translated_obs)

    print("""
    ------------------------------------------------------------------------------------
    - 2. Build prompt out of logical domain restrictions, plan, observations and query -    
    ------------------------------------------------------------------------------------
    """)

    llm_query = "Can you please analyse the plan and the given observations step-by-step and check for inconsistencies."
    anwer_form = "If the plan and the observations are consistent, please write as last line **CONSISTENT**. If they are not write **INCONSISTENT** and write a list of which action went wrong at what time stamp."
    answer_list = """
    This is how you should write the list:
    if e.g. at time step 4 move to b failed write, move(b) at T=4 failed
    if e.g. at time step 2 pickup package one failed write, pickup(one) at T=2 failed
    if e.g. at time step 5 release package two failed write, release(two) at T=5 failed
"""
    # if the move action failed, write: move(...) at T=... failed (e.g. at time step 4 move to b failed = move(b) at T=4 failed)
    # if the pickup action failed, write: pickup(...) at T=... failed (e.g. at time step 2 pickup package one failed = pickup(one) at T=2 failed)
    # if the release action failed, write: release(...) at T=... failed (e.g. at time step 5 release package two failed = release(two) at T=5 failed)
    final_prompt = makePrompt(
                    llm_constants.PREPROMPT_3,
                    llm_constants.PLAN_PREPROMT, 
                    translated_plan, 
                    llm_constants.OBSERVATION_PREPROMT,
                    translated_obs, 
                    llm_constants.FAULTS_AND_CAUSES, 
                    llm_constants.START_LOCATION, 
                    llm_constants.ADJACENT_LOCATIONS,
                    llm_query,
                    answer_denotation=anwer_form+answer_list
                    )   
    
    print(final_prompt)
    print("") 

    print("""
    ------------------------------------------------------------
    - 3. Query the LLM if plan and observations are consistent -    
    ------------------------------------------------------------
    """)
    print(llm_constants.LOADING_TEXT)
    response = queryLLM(final_prompt, show_stream=False)

    print(response['message']['content'])

    print("""
    -------------------------------
    - 4. Read in the LLM response -    
    -------------------------------
    """)

    if extractAnswer(response):
        print("Plan and Observations align!")
    else:
        print("Plan and Observations do NOT align!")
        answers = extractFaultyActions(response, llm_constants.PATTERNS)
        print(answers)
        
    time_end = time.time()
    dt = time_end-time_start
    minutes, seconds = divmod(dt, 60)
    print(f"Runtime Time: {int(minutes):02}:{int(seconds):02} (mm:ss)")