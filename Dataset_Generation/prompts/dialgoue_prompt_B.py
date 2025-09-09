def get_prompt(client, previous):
    prompt = f"""
        Generate a realistic dialogue between a client experiencing an acute panic attack and an online Psychological First Aid (PFA) counselor over a call.  
        The dialogue should reflect the **LISTEN Phase (Step B)** of the PFA Handbook, based on the **dialogue history** and the **counselor's plan**.

        ---

        ## Step B: LISTEN Phase (De-escalation Phase)

        The goal of this phase is to:
        - **[B.P1] Ensure Stability**: Help the client regain control through techniques like grounding or breathing.
        - **[B.P2] Reframing Perspective**: Help the client reinterpret catastrophic thoughts with rational, calming alternatives.

        The counselor’s plan outlines how these two goals will be achieved. Use that plan to guide the conversation.

        ---

        ## Counselor Behavior
        - Counselor responses must be based on the PFA Handbook and the counselor’s Step B plan.
        - If the client is highly distressed, focus first on **B.P1 (stabilization)**.
        - When the client begins to stabilize, gradually introduce **B.P2 (reframing perspective)**.
        - If the session is complete, mark the result as `MOVE`. Otherwise, use `KEEP`.

        ---

        ## Client Behavior
        - The client may initially struggle to follow instructions.
        - As stabilization progresses, their responses may become clearer and calmer.
        - If severity is high, simulate fragmented or gasping speech.

        ---

        ## Required Output Format

        Return the output in the following **JSON format**:

        ```json
        {{
          "possible_to_end_reasoning": "<Natural language reasoning that explains if B.P1 and B.P2 are complete, ending in MOVE or KEEP>",
          "counselor": "<counselor's utterance>"
          "client": "<client's response>",
        }}
        ```
        """
        return prompt