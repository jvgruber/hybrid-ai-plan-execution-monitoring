import llm_constants
import asp_constants

from asp_module import translateAnswerSet, printAnswerSet, solveASP
from llm_module import queryLLM, makePrompt

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

    plan = """
robot_at(0,a).
packet_at(8,one,b).
packet_at(1,one,b).
robot_at(1,b).
packet_at(5,two,2).
    """
    answer_sets = solveASP("asp_domain_modelling.pl", plan) # add time stemps
    printAnswerSet(answer_sets)