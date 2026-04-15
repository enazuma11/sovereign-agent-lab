"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking    
How many guests are you confirming for tonight's event?
Your input ->  160                                                                                                                                                                                        
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan   
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                                                                               
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->  no, thats it                                                                                                                                                                               
Okay, I'll be around in case you need further help.
? How would you rate your experience today? 1: 👍 Satisfied (/SetSlots(csat_score=satisfied))                                                                                                             
Thank you for your feedback! I'm glad I could help.
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """ 
Your input ->  calling to confirm a booking    
How many guests are you confirming for tonight's event?
Your input ->  160                                                                                                                                                                                        
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan   
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £589 deposit                                                                                                                                                                               
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £589 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £589 exceeds the organiser's authorised limit of £300. "   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
How many guests are you confirming for tonight's event?
Your input ->  60 guests                                                                                                                                                                                  
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?                                                                                                                                                  
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
It handled the scenario well, by skipping this question and reconfirming if I want to continue on my booking.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa CALM's handled the out-of-scope request well by skipping that request and restricting itself for the task it's designed for.
While in case of LangGraph agent, it went ahead and did the web search or whatever information it had wrt that out-of-scope question, 
it answered that leaving its designated task. It proves that Rasa's path is more deterministic while LangGraph is a bit more generic and flexible.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["sovereign-agent-lab/exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Making the condition True [the condition that asks for the current time and checks it should be greater than 16:45].
I tried testing that by running it after 16:45 in my local and it worked fine, strange.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
The primary gain is developer velocity and conversational resilience. 
By offloading extraction and dialogue management to the LLM, you no longer 
need to exhaustively map every possible synonym or dialogue path in nlu.yml 
and rules.yml. The LLM naturally handles "about 160" or mid-conversation 
interruptions that would have previously broken a rigid FormAction. 
This allows the developer to focus purely on business logic (the "Action" class) 
rather than linguistic edge cases.

Python still handles the ActionValidateBooking because while we trust LLMs to 
extract "160," we don't trust them to enforce specific business constraints—like 
checking if a venue actually has 160 chairs—without a verified database check.

"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The higher setup cost of Rasa Pro CALM buys you enterprise-grade reliability 
and conversational guardrails that LangGraph’s flexible code-first approach 
lacks. While LangGraph allows an agent to improvise, call any tool, or "loop" 
indefinitely, Rasa CALM forces the AI to follow prescriptive business logic 
defined in flows.yml.

Deterministic Outcomes: In the booking confirmation use case, the inability 
to "improvise" is a feature, not a limitation. It ensures that every guest is 
processed exactly according to your business rules (e.g., verifying capacity 
before confirming).

Ultimately, Rasa's setup ensures that even if the LLM is "smart," it remains 
a compliant representative of your business, whereas a LangGraph agent is a 
creative researcher that might wander off-script to solve a problem.
"""
