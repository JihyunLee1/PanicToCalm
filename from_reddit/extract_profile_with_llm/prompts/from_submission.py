def get_prompt(sns_text):
    """
    Generates a structured prompt for GPT-4 to extract key clinical information
    from a given SNS post describing a panic attack.

    Parameters:
        sns_text (str): The SNS post written by the patient.

    Returns:
        str: The formatted prompt for GPT-4.
    """
    
    prompt = f"""
        You are a professional mental health counselor specializing in anxiety disorders, particularly panic attacks.
        Before starting counseling, you need to extract key clinical information from a patient's SNS post.

        **SNS Post:**  
        "{sns_text}"

        Now extract the following information from the SNS post:
        **Output Format:** Provide the extracted information in JSON format, filling in values based on the given text. If certain information is unclear or not mentioned, set the value as `"unknown"`.
        
        **Expected Output Format:**  
        ```
        {{
            "environment": "Crowded subway",
            "trigger": "Feeling trapped, loud noises",
            "physical_symptom": "Heart racing, dizziness, shortness of breath",
            "emotional_react": "Overwhelmed, intense fear",
            "catastrophic_thought": "I’m going to die",
            "severity": "Extreme"
        }}
        ```
        If it is not about a panic attack (e.g., general anxiety or depression), please return:
        ```
        {{
            "NotAboutPanicAttack": "true"
        }}
        ```
    """

    return prompt.strip()
