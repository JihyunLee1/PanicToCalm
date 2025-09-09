# reference : https://github.com/coding-groot/cactus/blob/main/prompts/panas_before.txt


def get_prompt(client):
    prompt = f'''
        A person with the characteristics listed in the intake form received counseling. 
        Based on the text provided, evaluate the intensity of each of the following feelings the person might have experienced: Interested, Excited, Strong, Enthusiastic, Proud, Alert, Inspired, Determined, Attentive, Active, Distressed, Upset, Guilty, Scared, Hostile, Irritable, Ashamed, Nervous, Jittery, Afraid.

        For each feeling, generate a score from 1 to 5 using the following scale:
        1 - Very slightly or not at all
        2 - A little
        3 - Moderately
        4 - Quite a bit
        5 - Extremely

        Additionally, provide a brief explanation for each score. 

        Here is the text:
        {client}
    '''
    prompt += "The answer should be in the json fomat with brief explanation and score."
    prompt += "For example, {'Interested': {'explanation': 'The person was interested in the counseling session.', 'score': 4}, {'Excited': {'explanation': 'The person was excited to learn new things.', 'score': 3}, ...}"
    return prompt
