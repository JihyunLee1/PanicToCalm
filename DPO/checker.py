from transformers import AutoTokenizer

class Checker:
    def __init__(self, model_name, max_length):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.max_length = max_length
    
    def run(self, prompt):
        """Checks if the formatted conversation exceeds max_length."""
        
        messages = [
            {"role": "user", "content": prompt},
        ]
        formatted_text = self.tokenizer.apply_chat_template(messages, tokenize=False)
        tokenized = self.tokenizer(formatted_text, padding=False, truncation=False)
        
        # Check if token count exceeds max_length
        overflow = len(tokenized["input_ids"]) > self.max_length
        
        return overflow