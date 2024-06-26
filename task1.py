import llm_constants
import asp_constants

from asp_module import translateAnswerSet, printAnswerSet
from llm_module import queryLLM, makePrompt, extractAnswer

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

    print("""
    ---------------------------------------------------------------
    - 1. Translate the plan and observartions to natural language -    
    ---------------------------------------------------------------
    """)

    plan_1 = [['move(b)', 'pickup(one)','move(b)', 'move(b)', 'release(one)', 'pickup(two)', 'move(c)', 'move(b)', 'release(two)']]
    
    obs_1C = [['saw_packet_at(1,one).',':- saw_packet_at(3,P).', 'saw_packet_at(4,two).', ':- saw_packet_at(7,P).', ':- saw_packet_at(8,P).']]
    
    obs_1F = [['saw_packet_at(1,one).',':- saw_packet_at(3,P).', 'saw_packet_at(4,two).', ':- saw_packet_at(7,P).', 'saw_packet_at(8,one).']]

    PLAN = plan_1
    OBS = obs_1F

    translated_plan = translateAnswerSet(PLAN, asp_constants.INTERPRETER_RULES_TASK_2, 0)
    translated_obs = translateAnswerSet(OBS, asp_constants.INTERPRETER_RULES_TASK_2, 0)

    print(translated_plan, translated_obs)

    print("""
    ------------------------------------------------------------------------------------
    - 2. Build prompt out of logical domain restrictions, plan, observations and query -    
    ------------------------------------------------------------------------------------
    """)

    llm_query = "Can you please analyse the plan and the given observations step-by-step and check for inconsistencies."
    anwer_form = "If the plan and the observations are consistent, please wirte as last line **CONSISTENT**. If they are not wirte **INCONSISTENT** and write a list of which action went wrong at what time stamp."

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
                    answer_denotation=anwer_form
                    )   
    
    print(final_prompt)
    print("") 

    print("""
    ------------------------------------------------------------
    - 3. Query the LLM if plan and observations are consistent -    
    ------------------------------------------------------------
    """)
    print("The computer is working! The answer can not be displaysed while generating it. We are Sorry :/\n")
    response = queryLLM(final_prompt, show_stream=False)

    # response = {'model': 'llama3', 'created_at': '2024-06-26T13:20:22.993479032Z', 'message': {'role': 'assistant', 'content': "Let's go through the plan and observations step by step:\n\nAt time stemp 0: The robot moves to location b from current location A.\n\nObservation: None (since this is the first move)\n\nConsistency: **CONSISTENT**\n\nAt time stemp 1: Robot picks up package one at current location B.\n\nObservation: Robot observed package one\n\nConsistency: **CONSISTENT** (package one is indeed at location B)\n\nAt time stemp 2: The robot moves to location b from current location.\n\nObservation: None (since this move does not involve a packet being picked up or released)\n\nConsistency: **CONSISTENT**\n\nAt time stemp 3: The robot moves to location b from current location.\n\nObservation: Robot did not see a package\n\nConsistency: **INCONSISTENT** (package one should still be at location B, but the observation indicates it's missing. This could be due to a faulty pickup or release action)\n\nAt time stemp 4: Robot releases the package one at current location.\n\nObservation: Robot observed package two\n\nConsistency: **INCONSISTENT** (package one was released, but package two is being observed. This suggests that package two was not picked up correctly)\n\nAt time stemp 5: Robot picks up package two at current location.\n\nObservation: None (since this move does not involve a packet being picked up or released)\n\nConsistency: **CONSISTENT**\n\nAt time stemp 6: The robot moves to location c from current location.\n\nObservation: None (since this move does not involve a packet being picked up or released)\n\nConsistency: **CONSISTENT**\n\nAt time stemp 7: The robot moves to location b from current location.\n\nObservation: Robot did not see a package\n\nConsistency: **INCONSISTENT** (package two should still be at location C, but the observation indicates it's missing. This could be due to a faulty release action)\n\nAt time stemp 8: Robot releases the package two at current location.\n\nObservation: Robot observed package one\n\nConsistency: **INCONSISTENT** (package two was released, but package one is being observed. This suggests that package one was not released correctly earlier)\n\nThe actions that went wrong are:\n\n* At time stemp 3: A faulty release or pickup might have caused the package to disappear.\n* At time stemp 4: Package two was not picked up correctly.\n* At time stemp 7: A faulty release might have caused the package to remain on the robot.\n\nNote that these inconsistencies could be due to exogenous events (e.g., a wumpus moving packets) or faults in the robot's actions."}, 'done_reason': 'stop', 'done': True, 'total_duration': 150200287731, 'load_duration': 1146148, 'prompt_eval_count': 64, 'prompt_eval_duration': 6350656000, 'eval_count': 564, 'eval_duration': 143715264000}
    print(response['message']['content'])

    print("""
    -------------------------------
    - 4. Read in the LLM response -    
    -------------------------------
    """)

    if extractAnswer(response):
        print("Plan and Observations allign!")
    else:
        print("Plan and Observations do NOT allign!")
