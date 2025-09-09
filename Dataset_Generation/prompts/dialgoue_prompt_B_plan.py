
def get_prompt(client, history):
    prompt = f"""
        Generate a **counselor's plan** for Step B (De-escalation Phase) in a conversation between a client experiencing an acute panic attack and an online Psychological First Aid (PFA) counselor over a call.  
        Given dialogue history and counselor's last thought.

        ## **Counselor's Approach: Psychological First Aid (PFA) Handbook**  
        The counselor follows the **Psychological First Aid (PFA) Handbook**, starting with the **LISTEN Phase** (Step B).  
        Only generate a plan for **Step B (LISTEN Phase)** in this output.  

        ---

        ### **LISTEN Phase: De-escalation Phase**  
        The **LISTEN Phase** focuses on **actively engaging** with the client, providing emotional support, and guiding them through immediate de-escalation.  
        The counselor must complete all required elements (**B.P1, B.P2 **).  


        ### **Stabilization Process (Required)**
        - **[B.P1] Ensure Stability** → The counselor must help the client regain a sense of control using **grounding techniques or breathing exercises**.  
          - Grounding techniques : Feeling the texture of objects, Feeling the ground beneath you, Identifying objects, etc.
          - Breathing exercises : Deep breathing, Box breathing, etc.
        - **[B.P2] Reframing Perspective** → Help the client shift from **irrational fear** to a **more realistic and calming perspective**.  
          - Reinforce **safety, control, and the temporary nature of panic**.  
          - Avoid false reassurances—**acknowledge distress** while guiding the client toward a calmer state.  

        ---

        ### Example 1 ###
        When the dialgoue history is
        counselor : Hello this is first aid  center how may i help you?
        client : I'm stuck in this traffic, and I feel like I'm going to black out. My heart is racing, and I can't catch my breath!
        counselor : I understand that you're feeling really overwhelmed. Can you tell me what thoughts are going through your mind right now? Are you worried about something specific?
        client : I'm scared I'm going to collapse and pass out in this car. What if I can\u2019t get out? I feel so trapped!
        counselor : Thank you for sharing that. It's important that you feel safe right now. Are you able to hold onto something in your car, like the steering wheel, or can you pull over somewhere safe?
        client : I can hold onto the steering wheel, but the traffic is so bad. I feel like I can\u2019t breathe!

        IN this case the counselor's planning for step B should be
        ```json
        {{
            "counselor_plan": "The client feels trapped in traffic, heightening their panic. Since they are safe in the vehicle, I will first guide them through a grounding exercise, asking them to focus on gripping the steering wheel, the seat’s texture, and surrounding sounds. Once stabilized, I will introduce a box breathing technique (inhale-hold-exhale for four seconds each). Finally, I will reframe their fear, reminding them that while intense, their symptoms are temporary and not life-threatening, before transitioning to the next phase (Decatastrophizing)."
        }}
        ```

        Now generate the counselor's plan for Step B (De-escalation Phase) based on the provided dialogue history.

        - **Dialogue History**:  
          {{history}}
          
        Return the **counselor's plan** in the following JSON format:
            """
    return prompt