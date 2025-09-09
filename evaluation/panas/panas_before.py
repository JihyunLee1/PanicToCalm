# Reference: Code implementation inspired by
# https://github.com/coding-groot/cactus

import os
import pdb
import json
import argparse
from prompt.before import get_prompt
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import make_line, process_batch, process_live


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_type', type=str, default="live") # batch or live
    parser.add_argument("--llm_name", type=str, default = "gpt-4o")
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--client_path", type=str)
    args = parser.parse_args()
    return args

            
            
if __name__ == "__main__":
    args = parse_args()
    client_data = json.load(open(args.client_path))
    
    save_temp = f"./temp/client_panas.jsonl"
    save_result = f"batch_output/client_panas.jsonl"
    save_processed = f"{args.output_dir}/client_panas.json"
    
    os.environ["OPENAI_API_KEY"] = json.load(open("config.json"))["api-key"]
    if os.path.exists(save_temp):
        os.remove(save_temp)
    os.makedirs(os.path.dirname(save_temp), exist_ok=True)
    os.makedirs(os.path.dirname(save_result), exist_ok=True)
    os.makedirs(os.path.dirname(save_processed), exist_ok=True)
    
    print(f"🔥 Evaluate client panas")
    payloads = []
    
    for cid, client in client_data.items():
        line_id = f"{cid}"
        payload = make_line(line_id, get_prompt(client), model_name=args.llm_name)
        payloads.append(payload)
        with open(save_temp, "a") as f:
            f.write(json.dumps(payload) + "\n")

    if args.run_type == "batch":
        output = process_batch(save_temp, save_result)
    else:
        output = process_live(payloads)
        
        
    with open(save_processed, "w") as f:
        json.dump(output, f, indent=4)
    print("🌴 Done, Saved in", save_processed)