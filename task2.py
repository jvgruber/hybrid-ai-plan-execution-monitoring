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

    # Plans
    # plan = [['start(0,a)','move(1,b)','pickup(2,one)','move(3,c)','release(4,one)','move(5,b)','move(6,a)']]
    
    plan_1 = [['robot_at(A)', 'move(0,B)', 'pickup(1,one)','move(2,C)', 'move(3,E)', 'release(4,one)', 'pickup(5,two)', 'move(6,C)', 'move(7,B)', 'release(8,two)']]
    
    obs_1C = [['saw_packet_at(1,one).',':- saw_packet_at(3,P).', 'saw_packet_at(4,two).', ':- saw_packet_at(7,P).', ':- saw_packet_at(8,P).']]
    
    obs_1F = [['saw_packet_at(1,one).',':- saw_packet_at(3,P).', 'saw_packet_at(4,two).', ':- saw_packet_at(7,P).', 'saw_packet_at(8,one).']]
    
    # Observations
    # falty_observation = [['packet_at(0,empty,a)','packet_at(1,one, b)','packet_at(3,empty,c)','packet_at(5,one,b)','packet_at(6,empty,a)']]
    # correct_observation = [['packet_at(0,empty,a)','packet_at(1,one, b)','packet_at(3,empty,c)','packet_at(5,empty,b)','packet_at(6,empty,a)']]
    # loc_invariant_obs = [['saw_packet_at(1, one).', ':- saw_packet_at(3, P).', 'saw_packet_at(4, two).', ':- saw_packet_at(7, P).', 'saw_packet_at(8, one).']]

    PLAN = plan_1
    OBS = obs_1F

    print("""
    # -------------------------------------------------------------------
    # - 1. Translate the plan and the observartions to natural language -    
    # -------------------------------------------------------------------
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
    # -------------------------------------------------------------------
    # - 2. Generate a Prompt for the LLM --------------------------------
    # -------------------------------------------------------------------
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
    # -------------------------------------------------------------------
    # - 3. Query LLM ----------------------------------------------------
    # -------------------------------------------------------------------
    """)
    
    if llm_constants.SHOW_STREAM == False:
        print("The computer is working! The answer can not be displaysed while generating it. We are Sorry :/")
        
    response = queryLLM(prompt, show_stream=llm_constants.SHOW_STREAM) 

    if llm_constants.SHOW_STREAM:    
        for chunk in response:
            print(chunk['message']['content'], end='', flush=True)
    else:
        print(response['message']['content'])


    print("""
    # -------------------------------------------------------------------
    # - 4. Extract Answer -----------------------------------------------
    # -------------------------------------------------------------------
    """)

    consistent = extractAnswer(response)


    if not consistent:
        print("""The obsveratoins and plan are NOT consistent!\n - Generate possible action execution by giving the ASP solver the observations""")
        answer_sets = solveASP( "asp_domain_modelling.pl", OBS[0] )
        opti = answer_sets[-1]
        print( opti )
    else:
        print("The observations and the plan are consistent!")