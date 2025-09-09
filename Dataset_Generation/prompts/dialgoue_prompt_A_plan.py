def get_prompt(client): 
    f"""
    Generate the first utterance of the client and plan the counselor's approach, and write the counselor's note for the LOOK Phase (Step A) of the Psychological First Aid (PFA) Handbook.  
    This dialogue takes place over a call.
    ---

    ## Client's Profile  
    - Environment: {{client['environment']}}  
    - Physical Symptoms: {{client['physical_symptom']}}  
    - Emotion: {{client['emotional_react']}}  
    - Thought: "{{client['catastrophic_thought']}}"  
    - Triggers: {{client['trigger']}}  

    ---

    ## Counselor's Approach: Psychological First Aid (PFA) Handbook  
    The counselor follows the Psychological First Aid (PFA) Handbook, starting with the LOOK Phase (Step A).  
    Only generate a plan for Step A (LOOK Phase) in this output.  

    ### LOOK Phase: Information Gathering & Processing  
    The LOOK Phase focuses on assessing the client's condition and ensuring their safety.  
    - [A.Q1] Physical Symptoms  
    - [A.Q2] Emotional State  
    - [A.Q3] Catastrophic Thinking  
    - [A.P1] Ensure Safety (guide the client to a safe and quiet place based on their current environment)
    ---

    ## JSON Output Format  
    Return your output in the following format:

    ```json
    {{
    "client": "<Client's first utterance>",
    "counselor_plan": "<One-sentence plan covering physical symptoms, emotional state, catastrophic thinking, and immediate safety guidance.>"
    }}
    ```
    """
    return prompt