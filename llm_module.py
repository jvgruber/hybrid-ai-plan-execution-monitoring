import ollama
import re

def queryLLM(prompt="", model="llama3", temp=0.75, show_stream=False):
    # if len(prompt) == 0:
    #     print("Please set a Prompt, default is empty!")
    #     return ""
    # try:
    # else:
	response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}], stream=show_stream, )
	return response

    # except Exception as e:
    # 	return f"An error occurred: {e}"
	
def makePrompt(preprompt="", plan_prepromtpt="", plan=[""], observation_prepropt="" ,observaations=[""], faults_and_causes="", start_location="", adjacent_locations="", query="", answer_denotation=""):
    final_prompt = ""

    final_prompt += preprompt

    final_prompt += plan_prepromtpt
    for item in plan:
        final_prompt += (item + "\n")
    
    final_prompt += "\n"

    final_prompt += observation_prepropt
    for item in observaations:
        final_prompt += (item + "\n")

    final_prompt += "\n"

    final_prompt += faults_and_causes

    final_prompt += start_location
    final_prompt += adjacent_locations

    final_prompt += query

    final_prompt += answer_denotation

    return final_prompt

def extractAnswer(LLM_answer):
    content = LLM_answer['message']['content']
    if "**CONSISTENT**" in content:
        return True
    if "**INCONSISTENT**" in content:
        return False