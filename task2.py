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
    plan = [['start(0,a)','move(1,b)','pickup(2,1)','move(3,c)','release(4,1)','move(5,b)','move(6,a)']]
    
    # Observations
    falty_observation = [['packet_at(0,empty,a)','packet_at(1,one, b)','packet_at(3,empty,c)','packet_at(5,one,b)','packet_at(6,empty,a)']]
    correct_observation = [['packet_at(0,empty,a)','packet_at(1,one, b)','packet_at(3,empty,c)','packet_at(5,empty,b)','packet_at(6,empty,a)']]
    loc_invariant_obs = [['saw_packet_at(1, one).', ':- saw_packet_at(3, P).', 'saw_packet_at(4, two).', ':- saw_packet_at(7, P).', 'saw_packet_at(8, one).' ]]

    print("""
    # -------------------------------------------------------------------
    # - 1. Translate the plan and the observartions to natural language -    
    # -------------------------------------------------------------------
    """)
    plan_tanslater = translateAnswerSet(plan, asp_constants.INTERPRETER_RULES_TASK_2)
    
    print("Plan:")
    for item in plan_tanslater:
        print(item)

    observation_translated = translateAnswerSet(loc_invariant_obs, asp_constants.INTERPRETER_RULES_TASK_2)

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
    
    # if llm_constants.SHOW_STREAM == False:
    #     print("The computer is working! The answer can not be displaysed while generating it. We are Sorry :/")
        
    # response = queryLLM(prompt, show_stream=llm_constants.SHOW_STREAM) 

    # if llm_constants.SHOW_STREAM:    
    #     for chunk in response:
    #         print(chunk['message']['content'], end='', flush=True)
    # else:
    #     print(response['message']['content'])
    #     print(response)

    # print("LLM IS NOT CALLED, THE ANSWERS ARE STATIC!")

    response_consistent ={'model': 'llama3',
                'created_at': '2024-06-26T08:07:18.728795091Z',
                'message': {'role': 'assistant',
                'content': "Let's go through the plan and observations step-by-step:\n\nTime Step 0:\n* The robot starts at location A.\n* No preconditions or effects to check.\n\nTime Step 1:\n* The robot moves from location A to location B.\n* Precondition: Location B must be adjacent to location A. (OK)\n* Effect: Robot's new location is location B. (OK)\n\nObservation: At time stemp 1, the robot observed package one.\n\nConsistency check: The observation is consistent with the plan and the environment. Package one is indeed at location A, which the robot just left. **OK**\n\nTime Step 2:\n* The robot picks up package 1 at its current location (location B).\n* Precondition: Package 1 must be at location B, and the robot can only carry one package. (OK)\n* Effect: Robot picks up package 1. (OK)\n\nObservation: None.\n\nConsistency check: No observations to compare with the plan's effects. **OK**\n\nTime Step 3:\n* The robot moves from location B to location C.\n* Precondition: Location C must be adjacent to location B. (OK)\n* Effect: Robot's new location is location C. (OK)\n\nObservation: At time stemp 3, the robot did not see a package.\n\nConsistency check: This observation is consistent with the plan and environment. The robot has left location B, where package one was, so it's expected that the robot doesn't see any packages at this step. **OK**\n\nTime Step 4:\n* The robot releases the package (package 1) at its current location (location C).\n* Precondition: Robot must be carrying a package, and can only release one package. (OK)\n* Effect: Package 1 is placed at location C. (OK)\n\nObservation: At time stemp 4, the robot observed package two.\n\nConsistency check: This observation is inconsistent with the plan's effects. The plan releases package 1, but the robot observes package 2 instead. **CONSISTENT**\n\nTime Step 5:\n* The robot moves from location C to location B.\n* Precondition: Location B must be adjacent to location C. (OK)\n* Effect: Robot's new location is location B. (OK)\n\nObservation: None.\n\nConsistency check: No observations to compare with the plan's effects. **OK**\n\nTime Step 6:\n* The robot moves from location B to location A.\n* Precondition: Location A must be adjacent to location B. (OK)\n* Effect: Robot's new location is location A. (OK)\n\nObservation: At time stemp 8, the robot observed package one.\n\nConsistency check: This observation is consistent with the plan and environment. The plan releases package 1 at location C, but we don't know what happens to it afterwards. It's possible that someone moved it back to location A. **OK**\n\nTime Step 7:\n* No action is specified in the plan.\n* Observation: At time stemp 7, the robot did not see a package.\n\nConsistency check: This observation is consistent with the plan, as no actions are specified at this step. **OK**\n\nThe analysis reveals that the plan and observations are inconsistent at Time Step 4."}, 'done_reason': 'stop',
                'done': True, 
                'total_duration': 151484520864, 
                'load_duration': 1076148, 
                'prompt_eval_duration': 212420000, 
                'eval_count': 683, 
                'eval_duration': 151140465000}


    response_inconsistent ={'model': 'llama3',
                    'created_at': '2024-06-26T08:07:18.728795091Z',
                    'message': {'role': 'assistant',
                    'content': "Let's go through the plan and observations step-by-step:\n\nTime Step 0:\n* The robot starts at location A.\n* No preconditions or effects to check.\n\nTime Step 1:\n* The robot moves from location A to location B.\n* Precondition: Location B must be adjacent to location A. (OK)\n* Effect: Robot's new location is location B. (OK)\n\nObservation: At time stemp 1, the robot observed package one.\n\nConsistency check: The observation is consistent with the plan and the environment. Package one is indeed at location A, which the robot just left. **OK**\n\nTime Step 2:\n* The robot picks up package 1 at its current location (location B).\n* Precondition: Package 1 must be at location B, and the robot can only carry one package. (OK)\n* Effect: Robot picks up package 1. (OK)\n\nObservation: None.\n\nConsistency check: No observations to compare with the plan's effects. **OK**\n\nTime Step 3:\n* The robot moves from location B to location C.\n* Precondition: Location C must be adjacent to location B. (OK)\n* Effect: Robot's new location is location C. (OK)\n\nObservation: At time stemp 3, the robot did not see a package.\n\nConsistency check: This observation is consistent with the plan and environment. The robot has left location B, where package one was, so it's expected that the robot doesn't see any packages at this step. **OK**\n\nTime Step 4:\n* The robot releases the package (package 1) at its current location (location C).\n* Precondition: Robot must be carrying a package, and can only release one package. (OK)\n* Effect: Package 1 is placed at location C. (OK)\n\nObservation: At time stemp 4, the robot observed package two.\n\nConsistency check: This observation is inconsistent with the plan's effects. The plan releases package 1, but the robot observes package 2 instead. **INCONSISTENT**\n\nTime Step 5:\n* The robot moves from location C to location B.\n* Precondition: Location B must be adjacent to location C. (OK)\n* Effect: Robot's new location is location B. (OK)\n\nObservation: None.\n\nConsistency check: No observations to compare with the plan's effects. **OK**\n\nTime Step 6:\n* The robot moves from location B to location A.\n* Precondition: Location A must be adjacent to location B. (OK)\n* Effect: Robot's new location is location A. (OK)\n\nObservation: At time stemp 8, the robot observed package one.\n\nConsistency check: This observation is consistent with the plan and environment. The plan releases package 1 at location C, but we don't know what happens to it afterwards. It's possible that someone moved it back to location A. **OK**\n\nTime Step 7:\n* No action is specified in the plan.\n* Observation: At time stemp 7, the robot did not see a package.\n\nConsistency check: This observation is consistent with the plan, as no actions are specified at this step. **OK**\n\nThe analysis reveals that the plan and observations are inconsistent at Time Step 4."}, 'done_reason': 'stop',
                    'done': True, 
                    'total_duration': 151484520864, 
                    'load_duration': 1076148, 
                    'prompt_eval_duration': 212420000, 
                    'eval_count': 683, 
                    'eval_duration': 151140465000}

    print("""
    # -------------------------------------------------------------------
    # - 4. Extract Answer -----------------------------------------------
    # -------------------------------------------------------------------
    """)

    consistent = extractAnswer(response_inconsistent)


    if not consistent:
        print("""The obsveratoins and plan are NOT consistent!\n - Generate possible action execution by giving the ASP solver the observations""")
        answer_sets = solveASP( "asp_domain_modelling.pl", loc_invariant_obs[0] )
        opti = answer_sets[-1]
        print( opti )
    else:
        print("The observations and the plan are consistent!")