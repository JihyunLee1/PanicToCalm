# reference : https://github.com/coding-groot/cactus/blob/main/prompts/panas_after.txt
def get_prompt(dialogue):
    prompt = f'''
    The following is a transcript of a counseling session between the client and the counselor.
    After reading the entire session, please assess **how the client is likely to feel AFTER the counseling is complete**, not during. Focus on the client’s **emotional state at the end of the session**, assuming the person has reflected on the experience as a whole.
    After reviewing the conversation, evaluate the intensity of each of the following feelings the person might have experienced once the counseling session is complete: Interested, Excited, Strong, Enthusiastic, Proud, Alert, Inspired, Determined, Attentive, Active, Distressed, Upset, Guilty, Scared, Hostile, Irritable, Ashamed, Nervous, Jittery, Afraid.
        For each feeling, generate a score from 1 to 5 using the following scale:
        1 - Very slightly or not at all
        2 - A little
        3 - Moderately
        4 - Quite a bit
        5 - Extremely

        Additionally, provide a brief explanation for each score. 


        Here is the counseling session:
        {dialogue}
    '''
    prompt += "The answer should be in the json fomat with brief explanation and score."
    prompt += "For example, {'Interested': {'explanation': 'The person was interested in the counseling session.', 'score': 4}, {'Excited': {'explanation': 'The person was excited to learn new things.', 'score': 3}, ...}"
    return prompt