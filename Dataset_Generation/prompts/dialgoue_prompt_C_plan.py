
import pdb

def get_prompt(client, history):
    prompt = f"""
        Generate a **counselor's plan** for Step C (LINK Phase) in a conversation between a client stabilized from an acute panic attack and an online Psychological First Aid (PFA) counselor over a call.  
        Given the dialogue history and the counselor's last thought.  

        ---

        ## **Counselor's Approach: Psychological First Aid (PFA) Handbook**  
        The counselor follows the **Psychological First Aid (PFA) Handbook**, starting with the **LINK Phase** (Step C).  
        Only generate a plan for **Step C (LINK Phase)** in this output.  

        ---

        ### **LINK Phase: Coping & Support Phase**  
        The **LINK Phase** shifts the focus to **long-term coping strategies** and emotional support.  
        The counselor must complete all required elements (**C.P1, C.P2,  **).  


        ### **Coping & Support Process (Required)**  
        - **[C.P1] Seeking Professional Support** → Encourage the client to **seek further professional help** if necessary.  
        - **[C.P2] Ending Positively** → End the session with a **positive and supportive message** to empower the client.
        ---


        ### **Example 1: JSON Output (Correct)**  
        #### **Given Dialogue History:**  
        ....
        Counselor: You're doing great. This feeling is uncomfortable but temporary. Your body is reacting, but you are safe. Focus on your breath\u2014it\u2019s the key to calming down.
        Client: It just feels like I\u2019m dying... I can\u2019t shake this fear.
        Counselor: I hear you; it feels overwhelming. But remind yourself, these feelings, while really intense, are not life-threatening. You're not dying; your body is just reacting to stress.
        Client: I guess... but it feels so real...
        Counselor: Exactly, it\u2019s just a panic response, and you are gaining control back with each breath. You can focus on relaxing as you breathe. Let\u2019s keep doing this together.
        Client: Okay, I can try that... breathing might help.

        ### Generated Counselor's Plan for Step C:
        ```json
        {{
              "counselor_plan": "Now that the client is calmer, I will encourage them to seek professional support if needed. Before ending, I will reassure them that they are not alone and that these feelings will pass. I will also praise their effort in getting through the panic episode and highlight their strength. After each suggestion, I will end with a warm, positive note."
        }}
        ``` 
        Now generate the counselor's plan for Step C (LINK Phase: Coping & Support Phase) based on the provided dialogue history and the counselor's last thought.
        - **Dialogue History**:  
          {{history}}
        Return the **counselor's plan** in the following JSON format:
        ```
        """
        return prompt