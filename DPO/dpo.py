import os, glob, shutil
import json
import argparse
from datetime import datetime
from datasets import Dataset, DatasetDict
from datasets import Dataset
from trl import DPOTrainer, DPOConfig
import wandb
from transformers import TrainerCallback
import torch.nn.functional as F
from logger import Logger
from checker import Checker
import torch
from panic import Panic

os.environ["NCCL_P2P_DISABLE"] = "1"
os.environ["NCCL_IB_DISABLE"] = "1"
parser = argparse.ArgumentParser()
parser.add_argument('--demo_config_path', type=str, required=True)
parser.add_argument('--data_path', type=str)
parser.add_argument('--client_path', type=str)
parser.add_argument('--client_gpt', type=str, default="gpt-4o-mini")
parser.add_argument('--max_step', type=int, default=10)
parser.add_argument('--dpo_train_batch_size', type=int, default=2)
parser.add_argument('--dpo_eval_batch_size', type=int, default=2)
args = parser.parse_args()

class LogDPOCallback(TrainerCallback):
    def __init__(self, tokenizer, valid_dataset, num_samples=3, wandb_prefix="dpo_sample"):
        self.tokenizer = tokenizer
        self.valid_dataset = valid_dataset
        self.num_samples = num_samples
        self.wandb_prefix = wandb_prefix

    def get_logprob(self, model, input_text, target_text):
        """
        Compute average log-probability of target_text given input_text.
        """
        full_input = input_text + target_text
        tokenized = self.tokenizer(full_input, return_tensors="pt").to(model.device)
        input_ids = tokenized.input_ids
        attention_mask = tokenized.attention_mask

        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits[:, :-1, :]  # (B, L-1, V)
            labels = input_ids[:, 1:]

            log_probs = F.log_softmax(logits, dim=-1)
            chosen_log_probs = log_probs.gather(2, labels.unsqueeze(-1)).squeeze(-1)

            # mask out padding tokens
            loss_mask = (labels != self.tokenizer.pad_token_id)
            sum_logprob = (chosen_log_probs * loss_mask).sum()
            count = loss_mask.sum()

        avg_logprob = (sum_logprob / count).item()
        return avg_logprob

    def on_evaluate(self, args, state, control, **kwargs):
        model = kwargs["model"]

        for idx in range(min(self.num_samples, len(self.valid_dataset))):
            sample = self.valid_dataset[idx]

            prompt = sample["prompt"]
            chosen = sample["chosen"]
            rejected = sample["rejected"]
            messages = [    
            {"role": "user", "content": sample["prompt"]}
            ]
            # 🔹 모델 출력 생성
            formatted_input = self.tokenizer.apply_chat_template(messages, tokenize=False)
            prompt_ids = self.tokenizer(formatted_input, return_tensors="pt").input_ids.to(model.device)
            generated_ids = model.generate(prompt_ids, max_new_tokens=256)
            generated_ids = generated_ids[:, prompt_ids.shape[1]:]  # Remove the prompt part
            generated_output = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)

            # 🔹 Log-prob 계산
            chosen_logprob = self.get_logprob(model, prompt, chosen)
            rejected_logprob = self.get_logprob(model, prompt, rejected)

            model_pref = "chosen" if chosen_logprob > rejected_logprob else "rejected"

            log_text = f"""🔹 Sample {idx+1}
            🔸 Prompt:
            {prompt}

            ✅ Generated:
            {generated_output}

            🟢 Chosen:
            {chosen}

            🔴 Rejected:
            {rejected}

            📊 LogProbs:
            - chosen_logprob: {chosen_logprob:.4f}
            - rejected_logprob: {rejected_logprob:.4f}
            🎯 Model Preference: {model_pref}
            """
            
            print(log_text)
        return control
    
    
def setup_logging_and_config(args):
    demo_config = json.load(open(args.demo_config_path))
    os.makedirs(demo_config["dpo_model_dir"], exist_ok=True)
    return demo_config


def init_wandb(demo_config):
    current_time = datetime.now().strftime("%m%d_%H%M%S")
    wandb.init(project="pacer", name=f"pacer_{current_time}", config=demo_config)


def get_dpo_config(output_dir):
    return DPOConfig(
        output_dir = output_dir, 
        beta=0.1,
        learning_rate=1e-5,
        max_length=1024,
        num_train_epochs=3,
        logging_steps=10,
        report_to='wandb',
        evaluation_strategy="steps",
        save_strategy="steps",  # 또는 "steps"
        save_steps=100,
        eval_steps=100,
        per_device_train_batch_size=args.dpo_train_batch_size,
        gradient_accumulation_steps=4,
        per_device_eval_batch_size=args.dpo_eval_batch_size,
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="loss",
        greater_is_better=False
    )
    
def save_count_check(data_cache, max_count, file_extension=None):
    """
    Sorts the items in `data_cache` by creation time and deletes the oldest ones.
    
    - If `file_extension` is specified: only files with that extension are kept.
    - If `file_extension` is None: folders starting with 'step_' are kept.
    """

    if file_extension:  # ✅ 파일 처리
        items = [
            f for f in os.listdir(data_cache)
            if f.endswith(file_extension) and os.path.isfile(os.path.join(data_cache, f))
        ]
        get_time = lambda x: os.path.getctime(os.path.join(data_cache, x))
        delete_fn = lambda x: os.remove(os.path.join(data_cache, x))
        item_type = "file"

    else:  # ✅ 폴더 처리 (step_*)
        items = [
            f for f in os.listdir(data_cache)
            if f.startswith("step_") and os.path.isdir(os.path.join(data_cache, f))
        ]
        get_time = lambda x: os.path.getctime(os.path.join(data_cache, x))
        delete_fn = lambda x: shutil.rmtree(os.path.join(data_cache, x))
        item_type = "folder"

    # 정렬 및 삭제
    items_sorted = sorted(items, key=get_time)

    if len(items_sorted) > max_count:
        to_delete = items_sorted[:len(items_sorted) - max_count]
        for item in to_delete:
            delete_fn(item)
            print(f"🧹 Deleted old {item_type}: {item}")

def clear_cache_folder(cache_dir):
    items = glob.glob(os.path.join(cache_dir, "*"))  
    deleted = 0

    for item in items:
        if os.path.isfile(item):
            os.remove(item)
            deleted += 1
        elif os.path.isdir(item):
            shutil.rmtree(item)
            deleted += 1

    print(f"🧹 Deleted {deleted} items in {cache_dir}")
def load_filtered_dataset(path):
    with open(path, "r") as f:
        raw_data = json.load(f)

    dataset_dict = {}

    for split in ["train", "valid", "test"]:
        if split in raw_data:
            examples = raw_data[split]
            filtered = [
                {
                    "prompt": ex["prompt"],
                    "chosen": ex["chosen"],
                    "rejected": ex["rejected"]
                }
                for ex in examples
                if "prompt" in ex and "chosen" in ex and "rejected" in ex
            ]
            dataset_dict[split] = Dataset.from_list(filtered)

    return DatasetDict(dataset_dict)



        
def main():
    demo_config = setup_logging_and_config(args)
    init_wandb(demo_config)
    logger = Logger(demo_config['log_path'])
    checker = Checker(demo_config['base_model'], demo_config['max_length'])
    panic = Panic(demo_config, checker, logger)
    dpo_config = get_dpo_config(demo_config["dpo_model_dir"])
    panic.set_adapter("utt")
    

    # 1. Simulate new user and generate training data
    dataset = load_filtered_dataset(args.data_path)
    # sft_test(panic.model, panic.tokenizer, dataset['valid'])

    logger.log_and_print(f"\n🚀Len of dataset: {len(dataset['train'])}")
    # 2. Train PACER with DPO
    trainer = DPOTrainer(
        model=panic.model,
        args=dpo_config,
        train_dataset=dataset['train'],
        eval_dataset=dataset['valid'],
        tokenizer=panic.tokenizer,
    )
    trainer.add_callback(
    LogDPOCallback(
        tokenizer=panic.tokenizer,
        valid_dataset=dataset['valid'],
        num_samples=3  # 몇 개 찍을지 조정
        )
    )
    trainer.train()        
if __name__ == "__main__":
    main()
