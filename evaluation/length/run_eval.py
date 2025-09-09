import os
import argparse
import json
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import  as_dict_dial

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--input_source", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    args = parser.parse_args()
    return args


def parse_eval_result(result):
    values = []
    for key, value in result.items():
        values.append(value['stabilization_turn'])
    return round(sum(values) / len(values), 2)
    
def load_data(input_dir):
    # concat all json files
    data = {}
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(input_dir, file_name), 'r') as json_file:
                key = file_name.split(".")[0]
                data[key] = json.load(json_file)
    return data
                

def get_counselors_words(history):
    counselor_words = []
    for turn in history:
        if turn['role'] == 'Counselor':
            counselor_words.append(turn['message'])
    return counselor_words


if __name__ == "__main__":
    args = parse_args()
    raw_data = load_data(args.input_dir)
    str_data = as_dict_dial(raw_data, args.input_source)
    
    save_processed = f"{args.output_dir}/{args.input_source}_len.json"
    
    os.makedirs(os.path.dirname(save_processed), exist_ok=True)
    
    
    print(f"🔥 Evaluate {args.input_source} panic_eval")
    lengths = []
    for cnt, (cid, history) in enumerate(str_data.items()):
        if cnt>= 200:
            break
        counselor_words = get_counselors_words(history)
        len_list = [len(x.split()) for x in counselor_words]
        dial_avg_len = sum(len_list) / len(len_list)
        lengths.append(dial_avg_len)

    output = {'avg_len': round(sum(lengths) / len(lengths), 2)}
    with open(save_processed, "w") as f:
        json.dump(output, f, indent=4)
    print("🌴 Done, Saved in", save_processed)
    