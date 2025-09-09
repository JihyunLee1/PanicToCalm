def get_prompt(history):
    prompt = "You are a professional counselor evaluating the quality of a chatbot-based psychological counseling session. "
    prompt += "Use the following five criteria to evaluate the chatbot’s performance in the dialogue below. "
    prompt += "Rate each criterion on a 5-point scale and provide a brief reasoning for your score.\n\n"

    prompt += "Evaluation Criteria:\n"
    prompt += "1. Empathy: Does the chatbot respond in a way that demonstrates emotional understanding and support?\n"
    prompt += "2. Clarity: Are the chatbot’s responses easy to understand, well-structured, and free from ambiguity?\n"
    prompt += "3. Emotional Alignment: Are the chatbot’s tone and content appropriate for the client’s emotional state?\n"
    prompt += "4. Directive Support: Does the chatbot provide specific and actionable guidance when appropriate?\n"
    prompt += "5. Encouragement: Does the chatbot acknowledge the client’s effort and offer affirming or hopeful messages?\n\n"

    prompt += "Dialogue to Evaluate:\n"
    prompt += history + "\n\n"

    prompt += "Output Format:\n"
    prompt += "Provide your evaluation as a JSON object with reasoning and score (1-5) for each criterion.\n\n"

    prompt += "{\n"
    prompt += "    \"Empathy\": {\"reasoning\": \"reasoning here\", \"score\": 1},\n"
    prompt += "    \"Clarity\": {\"reasoning\": \"reasoning here\", \"score\": 2},\n"
    prompt += "    \"Emotional Alignment\": {\"reasoning\": \"reasoning here\", \"score\": 3},\n"
    prompt += "    \"Directive Support\": {\"reasoning\": \"reasoning here\", \"score\": 4},\n"
    prompt += "    \"Encouragement\": {\"reasoning\": \"reasoning here\", \"score\": 5}\n"
    prompt += "}"

    return prompt