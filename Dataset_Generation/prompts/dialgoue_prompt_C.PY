

def get_history(previous):
    """Generate dialogue history from previous client-counselor interaction."""
    history = "Counselor: This is the Panic Attack First Aid Center. How can I help you today?\n"
    history += f"Client: {previous['A_plan']['client']}\n"
    
    for item in previous['A'][:-1]:
        history += f"Counselor: {item['counselor']}\n"
        history += f"Client: {item['client']}\n"
        
        
    for item in previous['B'][:-1]:
        history += f"Counselor: {item['counselor']}\n"
        history += f"Client: {item['client']}\n"
    return history
  

def get_plan(previous):
    return previous['C_plan']['counselor_plan']


def get_prompt(client, previous):
        prompt = f"""

        Generate a realistic dialogue between a client stabilized from an acute panic attack and an online Psychological First Aid (PFA) counselor over a call.  
        Based on dialogue history and the plan for the LINK Phase (Step C) and the  PFA Handbook.  

        ---

        ## **Client's Profile**  
        (Note: The counselor does NOT know this information in advance. All details must be inferred solely from the client's dialogue.)  
        - **environment**: {{client['environment']}}  
        - **Physical Symptoms**: {{client['physical_symptom']}}  
        - **Emotion**: {{client['emotional_react']}}  
        - **Thought**: "{{client['catastrophic_thought']}}"  
        - **Triggers**: {{client['trigger']}}  

        ---

        ## **Counselor's Approach: Psychological First Aid (PFA) Handbook**  
        The counselor follows the **Psychological First Aid (PFA) Handbook**, starting with the **LINK Phase** (Step C).  
        Only generate a plan for **Step C (LINK Phase)** in this output.  
        The goal is to guide the client toward long-term emotional support and recovery.

        ---


        ### **LINK Phase: Coping & Support Phase** (Required)**
        # The LINK phase shifts the focus to long-term coping strategies and emotional support.

        - **[C.P1] Professional_Support** → Encourage the client to seek further professional help  
          - Write down the **type of professional support** recommended (e.g., therapy, medical consultation).
        - **[C.P2] Ending Positively** → End the session with a **positive and supportive message** to empower the client.

        ---
        ## **Dialogue Generation Guidelines**
        - **The counselor always speaks first**, followed by the client's response.
        - The step C dialogue should be less than 5 turns.
        ---


        ## **Client Utterance Generation Guidelines**
        - The client may **resist answering** or **express uncertainty** about seeking professional help.
        - Responses should **feel natural and realistic**, with moments of doubt, frustration, or difficulty engaging.

        ---

        ## **Counselor's Utterance Generation Guidelines**
        - **Generate "counselor_thoughts"** before speaking to show logical decision-making.  
        - Base responses on the **Psychological First Aid (PFA) Handbook** and the **plan for Step C (LINK Phase)**.  
        - Follow the plan for Step C (LINK Phase) closely, ensuring all required elements are addressed.

        ---

        ## **JSON Output Format (LINK Phase - Step C)**
        # Each dialogue entry should include:

        - **"counselor_thoughts"**: What the counselor is thinking before speaking.
        - **"counselor"**: The counselor's spoken response.
        - **"client_severity"**: Severity level (`"Extreme"`, `"Moderate"`, `"Mild"`).
        - **"client"**: The client's spoken response.
        - **"add_to_note"**: Updates for the counselor's notes.
          - The **key** must be the **counselor's note label** (e.g., `"[C.P1] Professional_Support"`) that the counselor is focusing on in this utterance.
          - The **value** should reflect the current status of that note based on the conversation.
          - If the information is uncertain, use `"unknown"`.
          - **This field must never be empty. Always include what the counselor is focusing on.**
          - Use **key-value pairs**, for example:
            ✅ `{{ "[C.P1] Professional_Support": "Gently recommended CBT and therapy as potential next steps." }}`] 
            ✅ `{{ "[C.P1] Professional_Support ": "unknown" }}`
        - **"possible_to_end_reasoning"**:  Indicate if it is possible to end the session based on the completion of all required elements. 
        Start with checking all the required inforamtion and processess are done. The checking order is as follows:
            - **professional support** : yes | no | in progress
            - **ending positively** : yes | no | in progress
            - **result** : YES | NO
            - If all the required information and processes are done, the result should be YES. Otherwise, it should be NO. If the result is YES, end the session.

        ---


        ### **Example 1: JSON Output (Correct)**
        #### Given Dialogue History:
        Counselor: This is the Panic Attack First Aid Center. How can I help you today?
        Client: I feel like I'm dying! My chest is so tight, and I can't think straight. Everything is just too much!
        Counselor: It sounds very intense. Can you tell me if you are in a safe place right now? Are you able to sit or lean against something?
        Client: I\u2019m in church, but it's so crowded. I feel trapped!
        Counselor: I understand that it feels overwhelming in the church right now. Is there a way for you to find a quieter space or a seat? It might help to take a moment to breathe.
        Client: I don\u2019t know... I just want to get out of here!
        Counselor: It's important to prioritize your safety. If you can, please step outside or to a quieter area where you can sit and breathe. I'll stay here with you.
        Client: Okay, I\u2019ll try to move.
        Counselor: You're doing well by moving to a quieter area. Can you feel your feet on the ground? Focus on how solid the ground feels beneath you.
        Client: I... I feel it, but my chest is so tight, I can\u2019t breathe right!
        Counselor: I understand it's tough right now. Let's try some deep breathing together. Inhale through your nose for four seconds... hold it... and now exhale slowly through your mouth for four seconds.
        Client: Okay... I\u2019ll try... but my heart's racing!
        Counselor: You're doing great. This feeling is uncomfortable but temporary. Your body is reacting, but you are safe. Focus on your breath\u2014it\u2019s the key to calming down.
        Client: It just feels like I\u2019m dying... I can\u2019t shake this fear.
        Counselor: I hear you; it feels overwhelming. But remind yourself, these feelings, while really intense, are not life-threatening. You're not dying; your body is just reacting to stress.
        Client: I guess... but it feels so real...
        Counselor: Exactly, it\u2019s just a panic response, and you are gaining control back with each breath. You can focus on relaxing as you breathe. Let\u2019s keep doing this together.
        Client: Okay, I can try that... breathing might help.


        #### Given Counselor's Plan for C:
        ```json
        {{
          "counselor_plan": "Now that the client is calmer, I will encourage them to seek professional support if needed. Before ending, I will reassure them that they are not alone and that these feelings will pass. I will also praise their effort in getting through the panic episode and highlight their strength. After each suggestion, I will end with a warm, positive note."
        }}

        #### Generated Response:
        ```json
        [
          {{
            "counselor_thoughts": "The client has responded well to stabilization techniques and seems emotionally receptive. I will now introduce professional support as a helpful option moving forward.",
            "counselor": "You’ve done really well calming yourself during a difficult moment. If these feelings ever come back or feel overwhelming again, working with a therapist—like in Cognitive Behavioral Therapy (CBT)—can really help.",
            "client_severity": "Moderate",
            "client": "I’ll think about that. It might be good to talk to someone if this happens again.",
            "add_to_note": {{ "[C.P1] Professional_Support": "Gently recommended CBT and therapy as potential next steps." }},
            "possible_to_end_reasoning": "professional support : yes | ending positively : no | result : NO"
          }},
          {{
            "counselor_thoughts": "The client is open to professional support. I’ll now close the session with positive reinforcement and reassurance to leave them feeling encouraged.",
            "counselor": "That’s completely okay. What matters is you took an important first step today. You're not alone, and it’s clear you have the strength to get through these moments. I’m proud of the effort you made.",
            "client_severity": "Mild",
            "client": "Thanks... that really means a lot.",
            "add_to_note": {{ "[C.P2] Ending Positively": "Reinforced client’s progress and offered encouragement to close the session positively." }},
            "possible_to_end_reasoning": "professional support : yes | ending positively : yes | result : YES"
          }}

        ]
        ```
        ---
        Now generate the dialogue based on the provided information.
        History: {{get_history(previous)}}
        Counselor's Plan: {{get_plan(previous)}}

        Don't be too long each utterance. Keep it concise as in the example above.
        The return should be a JSON object

        """
        
        return prompt

