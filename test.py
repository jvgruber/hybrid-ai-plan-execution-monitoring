import re
import llm_module
import llm_constants

text = """
Time stamp 8:
The robot releases package two at its current location B.
Precondition: The robot must be carrying a packet, but can not carry more than one package. (Met)
Effect: The robot places the package at its current location. (Expected outcome)

Observation: The robot observes package one at this time stamp.

Based on our analysis, we found that the plan and observations are inconsistent. **INCONSISTENT**

Here's a list of actions that went wrong:


"""

a = llm_module.extractFaultyActions(text, llm_constants.PATTERNS)
print(a)