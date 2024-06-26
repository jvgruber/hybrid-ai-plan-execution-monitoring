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
    
    # PLANS AND OBSERVATIONS
    plan_1 = [['move(b)', 'pickup(one)','move(b)', 'move(b)', 'release(one)', 'pickup(two)', 'move(c)', 'move(b)', 'release(two)']]
    
    obs_1C = [['saw_packet_at(1,one).',':- saw_packet_at(3,P).', 'saw_packet_at(4,two).', ':- saw_packet_at(7,P).', ':- saw_packet_at(8,P).']]
    
    obs_1F = [['saw_packet_at(1,one).',':- saw_packet_at(3,P).', 'saw_packet_at(4,two).', ':- saw_packet_at(7,P).', 'saw_packet_at(8,one).']]
    
    PLAN = plan_1
    OBS = obs_1F

    print("""
    -------------------------------------------------------------------
    - 1. Translate the plan and the observartions to natural language -    
    -------------------------------------------------------------------
    """)

    plan_tanslater = translateAnswerSet(PLAN, asp_constants.INTERPRETER_RULES_TASK_2)
    
    print("Plan:")
    for item in plan_tanslater:
        print(item)

    observation_translated = translateAnswerSet(OBS, asp_constants.INTERPRETER_RULES_TASK_2)

    print("Obs.:")
    for item in observation_translated:
        print(item)

    print("""
    -------------------------------------------------------------------
    - 2. Generate a Prompt for the LLM --------------------------------
    -------------------------------------------------------------------
    """)
    
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
    
    print("""
    -------------------------------------------------------------------
    - 3. Query LLM ----------------------------------------------------
    -------------------------------------------------------------------
    """)
    
    if llm_constants.SHOW_STREAM == False:
        print(llm_constants.LOADING_TEXT)
        
    response = queryLLM(prompt, show_stream=llm_constants.SHOW_STREAM) 

    if llm_constants.SHOW_STREAM:    
        for chunk in response:
            print(chunk['message']['content'], end='', flush=True)
    else:
        print(response['message']['content'])

    print("""
    -------------------------------------------------------------------
    - 4. Extract Answer -----------------------------------------------
    -------------------------------------------------------------------
    """)

    consistent = extractAnswer(response)

    if not consistent:
        print("""The obsveratoins and plan are NOT consistent!\n - Generate possible action execution by giving the ASP solver the observations""")
        answer_sets = solveASP( "asp_domain_modelling.pl", OBS[0] )
        opti = answer_sets[-1]
        print( opti )
    else:
        print("The observations and the plan are consistent!")