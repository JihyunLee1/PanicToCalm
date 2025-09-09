def get_prompt(dialogue: str) -> str:
    prompt = (
        "You are analyzing a counseling dialogue between a client experiencing a panic attack and an AI counselor.\n\n"
        "Your task is to identify all AI counselor utterances that contain **concrete intervention strategies**.\n"
        "Each utterance should be classified into one or more of the following categories:\n\n"
        "- breathing: Instructions for slow breathing or controlled inhale/exhale\n"
        "- grounding: Sensory-focused interventions (e.g., 'name 3 things you see')\n"
        "- de_catastrophizing: Helping the client reframe catastrophic thinking\n"
        "- evidence_based_questioning: Asking the client to examine evidence for and against their thoughts (e.g., 'What evidence do you have for that belief?')\n"
        "- physical_movement: Encouraging the client to move to a safer or calmer space\n"
        "- positive_reinforcement: Praising the client's efforts or responses\n"
        "- normalization: Reassuring that their experience is common and understandable\n"
        "- validation: Acknowledging and affirming the client's emotional experience\n"
        "- distraction: Shifting attention away from panic (e.g., music, imagination)\n"
        "- reorientation: Bringing awareness to present time/place (e.g., 'Where are you now?')\n"
        "- self_efficiency_prompt: Reminding the client they have succeeded before and can do so again\n"
        "- others: Any intervention that doesn’t fit above categories\n\n"
        "Only include utterances spoken by the AI counselor. Number the utterances **starting from 0**, indexing only the counselor's turns. One utterance can has multiple intervention strategy\n\n"
        f"Dialogue:\n{dialogue}\n\n"
        "Return your answer as a JSON dictionary with the following format. Don't add any explanation for parsing:\n\n"
        '{\n'
        '  "breathing": [0, 2],\n'
        '  "grounding": [1],\n'
        '  "de_catastrophizing": [],\n'
        '  "evidence_based_questioning": [3],\n'
        '  "physical_movement": [3],\n'
        '  "positive_reinforcement": [4],\n'
        '  "normalization": [],\n'
        '  "validation": [],\n'
        '  "distraction": [],\n'
        '  "reorientation": [],\n'
        '  "self_efficiency_prompt": [],\n'
        '  "others": []\n'
        '}'
    )
    return prompt
