# Reference: Code implementation inspired by
# https://github.com/coding-groot/cactus

import os
import argparse
import json
from prompt.after import get_prompt
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import make_line, process_batch, process_live, as_dial

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_type', type=str, default="batch") # batch or live
    parser.add_argument("--llm_name", type=str, default = "gpt-4o")
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--input_source", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--client", type=str)
    args = parser.parse_args()
    return args



def load_data(input_dir):
    # concat all json files
    data = {}
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(input_dir, file_name), 'r') as json_file:
                key = file_name.split(".")[0]
                data[key] = json.load(json_file)
    return data
                
    

 


if __name__ == "__main__":
    args = parse_args()
    raw_data = load_data(args.input_dir)
    str_data = as_dial(raw_data, args.input_source)
    client_data = json.load(open(args.client))
    
    save_temp = f"./temp/{args.input_source}_panas.jsonl"
    save_result = f"batch_output/{args.input_source}_panas.jsonl"
    save_processed = f"{args.output_dir}/{args.input_source}_panas.json"
    
    os.environ["OPENAI_API_KEY"] =API_KEY
    
    if os.path.exists(save_temp):
        os.remove(save_temp)
    os.makedirs(os.path.dirname(save_temp), exist_ok=True)
    os.makedirs(os.path.dirname(save_result), exist_ok=True)
    os.makedirs(os.path.dirname(save_processed), exist_ok=True)
    
    
    print(f"🔥 Evaluate {args.input_source} panas")
    payloads = []
    
    for cid, history in str_data.items():
        if len(payloads) == 200:
            break
        line_id = f"{cid}"
        payload = make_line(line_id, get_prompt(history), model_name=args.llm_name)
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