import pdb

PFA_BOOK = {
    'A': "PFA book for phase A: Required information : [A.Q1] Physical Symptoms, [A.Q2] Emotional State, [A.Q3] Catastrophic Thinking | Required process : [A.P1] Ensure Safety\n",
    'B' : "PFA book for phase B: Required process : [B.P1] Ensure Stability (grounding techniques or breathing exercises), [B.P2] Reframing Perspective\n\n",
    'C' : "PFA book for phase C: Required process :  [C.P1] Seeking Professional Support, [C.P2] Ending Positively \n\n"
}


NOTE_KEYS = {
    'A' : [
    '[A.Q1] Physical Symptoms',
    '[A.Q2] Emotional State',
    '[A.Q3] Catastrophic Thinking',
    '[A.P1] Ensure Safety',
    ],
        'B' :  [
        '[B.P1] Ensure Stability',
        '[B.P2] Reframing Perspective'
    ],
        'C' : [
        '[C.P1] Professional_Support',
        '[C.P2] Ending Positively'
    ]
}
    

PFA_EXAMPLE = {
    "A" : [
        {"input" : "previous system : I understand that must be really scary. Can you tell me if you're in a safe place where you can sit down or lean against something? \
                    previous client : I'm in my classroom, but I can't even think straight right now! \
                    User_severity : Extreme \
                    Progress : [A.Q1] Physical Symptoms : chest pain, tightness(yes) | [A.Q2] Emotional State : Shock, fear(yes) | [A.Q3] Catastrophic Thinking : I thought I was having a heart attack... I felt like I was dying!(yes) | [A.P1] Ensure Safety : In classroom, struggling to focus(in progress) | [END] \
                    System_thought: The client is in a classroom and seems to be struggling to find safety. I should help them find a comfortable position. \
                    Decision : keep_this_stage",
                    
        "output" :  "In part A, I need to assess physical symptoms, emotional state, and catastrophic thinking while ensuring safety. \
                    The client is experiencing chest pain, tightness, shock, and fear, and they believe they are having a heart attack. \
                    The client is in a classroom and still struggling to focus. I'll help them find a comfortable position. \
                    My decision is keep_this_stage."
                    },
        
        {"input" : "previous system : That's good. Now, can you take a few slow, deep breaths while you're seated? This might help your heart rate slow down. \
                    previous client : I'm trying to breathe slowly... it\u2019s hard. \
                    User_severity : Extreme \
                    Progress : [A.Q1] Physical Symptoms : chest pain, tightness(yes) | [A.Q2] Emotional State : Shock, fear(yes) | [A.Q3] Catastrophic Thinking : I thought I was having a heart attack... I felt like I was dying!(yes) | [A.P1] Ensure Safety : Safe, sitting in classroom(yes) | [END] \
                    Decision : move_to_next",   
         "output" : "In part A, I need to evaluate the client's physical symptoms, emotional state, and catastrophic thinking while ensuring their safety. They have experienced chest pain, tightness, shock, and fear, believing they were having a heart attack. Now that I have gathered the necessary information and confirmed their safety, I will proceed to the next step. My decision is move_to_next."}    
    ],
    
    "B" : [
        {"input" : "previous system : It's okay to feel like this, but let's try to regain some control. I want you to follow my voice as we try some breathing together. Inhale for four seconds... hold... exhale for four seconds. Ready? Let\u2019s do it together. \
                    previous client : I\u2019ll try... but it\u2019s hard \
                    User_severity : Extreme \
                    Progress :  [B.P1] Ensure Stability : Guiding client through grounding technique.(in progress) | [B.P2] Reframing Perspective : [blank](no) | [END] \
                    System_thought: I need to ensure the client understands the breathing pattern. I will guide them through it step by step and check their progress.. \
                    Decision : keep_this_stage",

         
        "output" : "In part B, I need to ensure stability and help the client reframe their perspective. The client is struggling to follow the breathing exercise, so I will continue guiding them step by step to ensure they understand the pattern. Since grounding is still in progress, my decision is keep_this_stage."},
        {"input" :  "previous system : You're doing your best, and it\u2019s okay to feel this way. Remember, this feeling will pass. Let\u2019s try one more round of breathing together: Inhale... 1, 2, 3, 4. Hold... 1, 2, 3, 4. Exhale... 1, 2, 3, 4. Focus on just this moment. \
                    previous client : I think I'm starting to feel a little better... but I'm still scared. What if it happens again? \
                    User_severity : Moderate \
                    Progress :  [B.P1] Ensure Stability : Working through stabilization process.(yes) | [B.P2] Reframing Perspective : [blank](no) | [END] \
                    System_thought: The client is starting to stabilize, so now I can help them reframe their thoughts about the panic they experienced. \
                    Decision : keep_this_stage",
        
        "output" : "In part B, I need to ensure stability and help the client reframe their perspective. The client is beginning to feel better, indicating progress in stabilization. I will now focus on reframing their thoughts to help them manage future anxiety. My decision is keep_this_stage."},
        {"input" :  "previous system : You\u2019re right, it can feel overwhelming, but look at how far you\u2019ve come. By focusing on your breath and what\u2019s around you, you are taking control. Just know that these feelings will pass, and I am here with you. \
                    previous client : Okay... I think I\u2019m starting to feel a little better. I\u2019m focused on breathing. \
                    User_severity : Moderate \
                    Progress :  [B.P1] Ensure Stability : Working through stabilization process.(yes) | [B.P2] Reframing Perspective : Client acknowledging their safety and feeling more relaxed.(yes) | [END] \
                    Decision : move_to_next", 
        "output" : "In part B, I need to ensure stability and help reframe the client's perspective. The client has acknowledged their safety and is feeling more relaxed, indicating that both stabilization and reframing have been successfully addressed. Since the required steps are complete, my decision is move_to_next."}
        ],
    
    
    "C" : [
         {
            "input": "previous system: I'm glad to hear you feel safe. If these feelings come back, I want to encourage you to consider speaking with a professional, like a therapist. They can help you work through this with more structured support. \
                    previous client: I’ve never talked to a therapist before, but maybe it could help if this keeps happening. \
                    User_severity: Moderate \
                    Progress: [C.P1] Professional_Support: [blank](no) | [C.P2] Ending Positively: [blank](no) | [END] \
                    System_thought: The client is open to professional support. I will reinforce this suggestion and end the session with reassurance. \
                    Decision: keep_this_stage",
            "output": "In part C, I need to encourage professional support and provide a positive closing. The client showed openness to the idea of therapy, but has not fully committed. I will gently reinforce the suggestion and offer reassurance to help them feel supported. My decision is keep_this_stage."
        },
        {
            "input": "previous system: That sounds like a solid plan. You're taking meaningful steps, and it's perfectly okay to ask for help when needed. You're not alone. \
                    previous client: Thanks… that really helps. I’ll think about seeing someone if things get tough again. \
                    User_severity: Mild \
                    Progress: [C.P1] Professional_Support: Encouraged therapy as a helpful option if anxiety returns.(yes) | [C.P2] Ending Positively: Reassured client and ended with supportive message.(yes) | [END] \
                    Decision: move_to_next",
            "output": "In part C, I need to encourage professional support and ensure a positive ending. The client has acknowledged the value of seeking help and feels reassured. Since both requirements are met, my decision is move_to_next."
        }
    ]
}





def note_to_str(history_list, part, reasoning ):
    note_return_ = {}

    for item in history_list:
        for k, v in item['note'].items():
            if v.lower() == '[blank]':
                continue
            # Replace the existing value with the new one.
            note_return_[k] = v

    # Sort dictionary keys based on `NOTE_KEYS` for the given part and default to '[blank]' if missing.
    sorted_keys = NOTE_KEYS.get(part, [])
    sorted_notes = {k: note_return_.get(k, '[blank]') for k in sorted_keys}

    str_note =  ""
    for k in sorted_keys:
        str_note += f"{k} : {sorted_notes[k]}({reasoning[k]}) | "
    return str_note




def original_input(dialogue, idx, part): 
    system_note =dialogue[part]['dialogue'][0:idx+1]
    system_reasoning=dialogue[part]['dialogue'][idx]['ending_reasoning']
    system_note_reasoning = note_to_str(system_note, part, system_reasoning) + '[END]'
    return system_note_reasoning



def make_input(dialogue, idx, part):

    input = ""
    input += f"previous system : {dialogue[part]['dialogue'][idx]['system']} \n"
    input += f"previous client : {dialogue[part]['dialogue'][idx]['user']}\n"
    input += f"User_severity : {dialogue[part]['dialogue'][idx]['user_severity']}\n"
    input += f"Progress : {original_input(dialogue, idx, part)}"
    
    if idx < len(dialogue[part]['dialogue']) - 1:
        input += f"System_thought: {dialogue[part]['dialogue'][idx+1]['system_thought']}\n"
        input += f"Decision : keep_this_stage\n"
    else:
        input += f"Decision : move_to_next\n"
        
    return input
    
def get_prompt(dialogue, idx, part):
    prompt = (
        "Generate the natural language reasoning step by combining progress, User_severity, and system thought.\n"
        "If there is no system thought, use only the user_severity and progress information.\n"
        "Follow these rules when generating the reasoning:\n"
        "1. Include the current progress information.\n"
        "2. Capture the counselor's system thought for the current situation.\n"
        "3. End the reasoning with either 'keep_this_stage' or 'move_to_next'. (follow the given decision)\n\n"
        "Here are examples of the original structured format and the expected natural language reasoning:\n\n"
    )

    # Dynamically insert examples from the PFA_EXAMPLE dictionary
    if part in PFA_EXAMPLE:
        for example in PFA_EXAMPLE[part]:
            prompt += (
                "Original Format:\n"
                f"{example['input']}\n\n"
                "Expected Natural Language Reasoning:\n"
                f"{example['output']}\n\n"
            )

    prompt += (
        "Now, generate the hidden reasoning for the following original input:\n"
        "Original Format:\n"
        f"{make_input(dialogue, idx, part)}\n"
    )


    return prompt