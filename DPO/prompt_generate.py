import json

static = json.load(open("assets/statics.json"))
PFA_BOOK = static['PFA_BOOK']
PFA_PHASE = static['PFA_PHASE']
NOTE_KEYS = static['NOTE_KEYS']

    
# history_list = history_for_plan(dialogue, part, last=3)
    
def plan_prompt(history_str, part): # checked
    user = f"Generate the counselor's first aid plan for phase {part} ({PFA_PHASE[part]}) based on the given information.\n\n"
    user += PFA_BOOK[part]
    user += f"History : \n {history_str}\n"
    return user

def policy_prompt(history_str, part, plan): # checked
    user = f"Generate the counselor's  reasoning for {part} step ({PFA_PHASE[part]}) to determine keep_this_stage or move_to_next.\n\n"
    user += PFA_BOOK[part]
    user += f"Plan for {part}: {plan}\n"
    user += f"History : \n {history_str}\n"
    
    return user


def utt_prompt(history_str, part, plan, run_options): # checked

    user = f"Generate the counselor utterance for phase {part} ({PFA_PHASE[part]}) based on the given information.\n\n"
    user += PFA_BOOK[part]
    if run_options['use_plan']:
        user += f"Plan for {part}: {plan}\n"
    user += f"History : \n {history_str}\n"
    return user