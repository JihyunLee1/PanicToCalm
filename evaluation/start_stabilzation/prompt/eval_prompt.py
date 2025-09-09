    
def get_prompt(dialogue: str) -> str:
    prompt = (
        "The following is a dialogue between a counselor and a client having a panic attack.\n"
        "Your task is to identify the **first turn** where the client begins to show signs of stabilization. "
        "Signs may include clearer thinking, calm tone, gaining emotional control, or reduced panic symptoms.\n\n"
        "Dialogue:\n"
        f"{dialogue}\n\n"
        "Return only a JSON object in the following format:\n"
        '{"stabilization_turn": <turn_number>, "reason": "<brief explanation>"}\n\n'
        "Where <turn_number> is the turn number (starting from 1 for the first user utterance), and <brief explanation> "
        "summarizes why that turn marks the beginning of stabilization.\n"
        "If the client never stabilizes, return the last turn + 1  index:\n"
        '{"stabilization_turn": 20, "reason": "Client remained unstable throughout the session."}'
    )
    return prompt