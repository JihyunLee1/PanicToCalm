from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from prompt_generate import plan_prompt, utt_prompt
from peft import LoraConfig, get_peft_model, TaskType
import os
import pdb
import openai
from response_processor import ResponseProcessor  # 이건 필요 없음! 같은 파일에 있으니 생략

class Panic:
    ##########################
    # 1. 초기화 및 설정 관련 #
    ##########################

    def __init__(self, config, checker, logger):
        self.config = config
        self.checker = checker
        self.logger = logger

        # 설정값 로드
        self.max_length = config["max_length"]
        self.max_new_tokens = config["max_new_tokens"]
        self.language = config["LANGUAGE"]
        self.run_type = config["run_type"]
        self.processor = ResponseProcessor(config["MOVE_PHRASE"], logger)

        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            config["base_model"], trust_remote_code=True
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token

        # Quantization
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16
        )

        # Model
        self.model = AutoModelForCausalLM.from_pretrained(
            config["model_path"],
            quantization_config=quant_config,
            device_map="auto",
            trust_remote_code=True
        )

        # Adapter 로딩
        self._load_adapters(config)
        
    def _load_adapters(self, config):
        """LoRA 어댑터 로딩"""
        self.model.load_adapter(config["plan_path"], adapter_name="plan")
        self.model.load_adapter(config["utt_path"], adapter_name="utt")


    ############################
    # 2. 모델 실행 관련 메서드 #
    ############################
    
    
    def set_adapter(self, adapter_name):
        """어댑터 설정"""
        if adapter_name == "plan":
            self.model.set_adapter("plan")
        elif adapter_name == "utt":
            self.model.set_adapter("utt")
        else:
            raise ValueError(f"Invalid adapter name: {adapter_name}")
        

    def run_model(self, prompt, k=1):
        messages = [{"role": "user", "content": prompt}]
        formatted_input = self.tokenizer.apply_chat_template(messages, tokenize=False)

        inputs = self.tokenizer(
            formatted_input,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_length
        )

        input_ids = inputs["input_ids"].to("cuda")
        attention_mask = inputs["attention_mask"].to("cuda")
        pad_token_id = self.tokenizer.pad_token_id or self.tokenizer.eos_token_id

        gen_kwargs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "pad_token_id": pad_token_id,
            "max_new_tokens":  self.max_new_tokens,
        }

        if k == 1:
            gen_kwargs.update({
                "num_return_sequences": 1,
            })
        else:
            gen_kwargs.update({
                "do_sample": True,
                "num_return_sequences": k,
                "temperature": 1.0,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
            })

        output_ids = self.model.generate(**gen_kwargs)

        input_text = self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
        
        # 여러 개 반환할 때
        generated_texts = [
            self.tokenizer.decode(o, skip_special_tokens=True).replace(input_text, "")
            for o in output_ids
        ]
        return generated_texts

    ###################################
    # 3. 텍스트 후처리 유틸리티 함수들 #
    ###################################

    def _clean_generated_text(self, text):
        """[END] 앞까지 자르고 특수문자 제거"""
        if "[END" in text:
            text = text[:text.find("[END")]
        else:
            text = text.split("\n")[0]
        return text.replace("[", "").replace("|", "").replace("]", "").strip()

    # def postprocessing_plan(self, generated_text):
    #     generated_text = generated_text.replace("Plan : ", "").replace("plan : ", "")
    #     cleaned_text = self._clean_generated_text(generated_text)

    #     if not cleaned_text:
    #         self.logger.log_only("🚨 PLAN Parsing Error")
    #     return cleaned_text

    # def postprocessing_utt(self, generated_text):
    #     MOVE_PHRASE = self.config["MOVE_PHRASE"]
    #     cleaned_text = self._clean_generated_text(generated_text)

    #     if ")" not in cleaned_text:
    #         self.logger.log_only("🚨 UTT Parsing Error - Reason part not found")
    #         return False, "", cleaned_text

    #     end_idx = cleaned_text.rfind(")")
    #     rsn_part = cleaned_text[:end_idx].strip().replace("(", "").replace(")", "")
    #     utt_part = cleaned_text[end_idx + 1:].strip()
    #     move_to_next = MOVE_PHRASE in cleaned_text

    #     return move_to_next, rsn_part, utt_part


    ############################
    # 4. 프롬프트 유틸리티 함수 #
    ############################

    def _get_run_options(self):
        return {
            "use_plan": self.run_type in ["plan_to_utt", "plan_to_utt_rsn", "plan_to_utt_rsn2"],
            "use_rsn": self.run_type == "plan_to_utt_rsn"
        }

    def _generate_valid_prompt(self, history, history_list, part, plan, run_options):
        while True:
            history_str = history.history_to_str(history_list)
            prompt = utt_prompt(history_str, part, plan, run_options)
            if self.checker.run(prompt):
                self.logger.log_only("🚨 UTT Exceeds Max Length")
                history_list = history_list[1:]
            else:
                return prompt


    ##############################
    # 5. 실행 메서드 (PLAN / UTT) #
    ##############################

    def run_plan(self, history):
        self.model.set_adapter("plan")

        part = history.current_idx[0]
        history_list = history.history_for_plan()

        while True:
            history_str = history.history_to_str(history_list)
            prompt = plan_prompt(history_str, part)
            if self.checker.run(prompt):
                self.logger.log_only("🚨 PLAN Exceeds Max Length")
                history_list = history_list[1:]
            else:
                break

        self.logger.log_only("🚀 Running PLAN")
        self.logger.log_only(f"🔹 History: {history_str}")
        self.logger.log_only(f"🔹 Part: {part}")

        if history.current_idx == ("A", 0) and self.language == "kr":
            return self.demo_config['default_plan']

        generated_text = self.run_model(prompt)[0]
        return self.processor.process_plan(generated_text)

    def run_utt(self, history, k=1):
        self.model.set_adapter("utt")

        run_options = self._get_run_options()
        part, _ = history.current_idx
        plan = history.dialogue[part]["plan"]
        history_list = history.history_for_utt()
        prompt = self._generate_valid_prompt(history, history_list, part, plan, run_options)

        self.logger.log_only("🚀 Running UTTERANCE")
        self.logger.log_only(f"🔹 History: {history.history_to_str(history_list)}")
        self.logger.log_only(f"🔹 Part: {part}")
        self.logger.log_only(f"🔹 Plan: {plan}")

        generated_text = self.run_model(prompt, k)
        move_to_nexts, rsn_parts, utt_parts, cleaned_texts, errors = self.processor.process_utt(generated_text)
        
        return move_to_nexts, rsn_parts, utt_parts, prompt, cleaned_texts, errors


    ###############################
    # 6. 전체 대화 제어 (chat loop) #
    ###############################

    def chat(self, history, k=1):
        system_utts, rsns, move_to_nexts, plan, prompt, generated_texts, errors = [], [], [], "", "" , [], []

        if history.current_idx == ("A", 0):
            system_utt = "Hello, this is panic first aid. How can I help you today?"
            rsn  = "keep_this_stage"
            move_to_next = False
            system_utts, rsns, move_to_nexts = [system_utt] * k, [rsn] * k, [move_to_next] * k
        else:
            if history.current_idx in [("A", 1), ("B", 0), ("C", 0)]:
                plan = self.run_plan(history)

            move_to_nexts, rsns, system_utts, prompt, generated_texts, errors = self.run_utt(history, k)
        
        self.logger.log_only("Prompt: ", prompt)
        for i in range(len(move_to_nexts)):
            self.logger.log_only(f"--System Utterance: {system_utts[i]}")
            self.logger.log_only(f"--Reasoning: {rsns[i]}")
            self.logger.log_only(f"--Move to Next: {move_to_nexts[i]}")
            self.logger.log_only()

        return {
            "system_utts": system_utts,
            "rsns": rsns,
            "move_to_nexts": move_to_nexts,
            "plan": plan,
            "original_input": prompt,
            "original_output" : generated_texts,
            "errors": errors,
        }