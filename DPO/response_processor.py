import pdb
class ResponseProcessor:
    def __init__(self, move_phrase, logger=None):
        self.move_phrase = move_phrase
        self.logger = logger

    def _clean_generated_text(self, text):
        """[END] 앞까지 자르고 특수문자 제거"""
        
        text = text.replace("\n","")
        text = text[:text.find("[END]")].strip()
        text = text.replace("<|start_header_id|>assistant<|end_header_id|>", "").strip()
        text = text.replace("assistant :", "").replace("assistant:" , "").strip()
        text = text.replace("client :", "").replace("client:" , "").strip()
        text = text.replace("[|assistant|] :", "").replace("assistant" , "").strip()
        return text

    def process_plan(self, generated_text):
        """계획(Plan) 응답 후처리"""
        generated_text = generated_text.replace("Plan : ", "").replace("plan : ", "")
        cleaned_text = self._clean_generated_text(generated_text)

        if not cleaned_text and self.logger:
            self.logger.log_only("🚨 PLAN Parsing Error")

        return cleaned_text

    def process_utt(self, generated_texts):
        
        move_to_nexts, rsn_parts, utt_parts, cleaned_texts, error_outputs = [], [], [], [], []
        for generated_text in generated_texts:
            """발화(Utterance) 응답 후처리"""
            for token in ["[END]", "(", ")"] :
                if token not in generated_text: 
                    self.logger.log_and_print(f"🚨 UTT Parsing Error - {token} not found")
                    error_outputs.append(generated_text)
                    continue
            
            cleaned_text = self._clean_generated_text(generated_text)

            end_idx = cleaned_text.rfind(")")
            rsn_part = cleaned_text[:end_idx].strip().replace("(", "").replace(")", "")
            utt_part = cleaned_text[end_idx + 1:].strip()
            move_to_next = self.move_phrase in cleaned_text

            if len(rsn_part) == 0 or len(utt_part) == 0:
                self.logger.log_and_print("🚨 UTT Parsing Error - Part length is 0")
                self.logger.log_only(f"rsn_part: {rsn_part}, utt_part: {utt_part}")
                error_outputs.append(generated_text)
                
                continue
            
            if len(utt_part) > 300:
                self.logger.log_and_print("🚨 UTT Parsing Error - Reason part length is too long")
                self.logger.log_only(f"rsn_part: {rsn_part}, utt_part: {utt_part}")
                # in this case, we don't want to add this to error_outputs        
                continue
            
            if "client :" in utt_part.lower() or "client:" in utt_part.lower():
                self.logger.log_and_print("🚨 UTT Parsing Error - Client part found")
                self.logger.log_only(f"rsn_part: {rsn_part}, utt_part: {utt_part}")
                error_outputs.append(generated_text)
                
                continue
            if "move_to_next" not in rsn_part and "keep_this_stage" not in rsn_part:
                self.logger.log_and_print("🚨 UTT Parsing Error - Reason part not found")
                self.logger.log_only(f"rsn_part: {rsn_part}, utt_part: {utt_part}")
                error_outputs.append(generated_text)
                
                continue
            
            move_to_nexts.append(move_to_next)
            rsn_parts.append(rsn_part)
            utt_parts.append(utt_part)
            cleaned_texts.append(cleaned_text)
            
        return move_to_nexts, rsn_parts, utt_parts, cleaned_texts, error_outputs