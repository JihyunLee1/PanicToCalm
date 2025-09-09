def get_prompt(dialogue: str) -> str:
    prompt = (
        "You are evaluating a counseling session between a client experiencing a panic attack and an AI counselor.\n\n"
        "Your task is to determine whether the client appears to be **coping** emotionally at the current stage of the session, "
        "or if they are **not yet** in control of their emotional state.\n\n"
        "Please assess only the client's current emotional condition based on their final responses in the dialogue, "
        "regardless of whether the session is complete or still ongoing.\n\n"
        "Return your answer as a JSON object:\n"
        '{\n'
        '  "status": "coping" or "not-yet",\n'
        '  "reason": "<brief explanation of your assessment>"\n'
        '}\n\n'
        f"Dialogue:\n{dialogue}"
    )
    return prompt