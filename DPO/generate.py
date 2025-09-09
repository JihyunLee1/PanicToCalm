import os, glob, shutil
import json
import argparse
from datetime import datetime
from ai_client import AI_CLIENT
import traceback

from history import History
from logger import Logger
from checker import Checker

from panic import Panic

from data_construction import Data_Construction
os.environ["NCCL_P2P_DISABLE"] = "1"
os.environ["NCCL_IB_DISABLE"] = "1"
parser = argparse.ArgumentParser()
parser.add_argument('--gpt_config_path', type=str)
parser.add_argument('--demo_config_path', type=str)
parser.add_argument('--client_path', type=str)
parser.add_argument('--client_gpt', type=str, default="gpt-4o-mini")
parser.add_argument('--max_num', type=int, default=30)
parser.add_argument('--fake_seed', type=int)
args = parser.parse_args()

def setup_logging_and_config(args):
    generate_config = json.load(open(args.demo_config_path))
    gpt_config = json.load(open(args.gpt_config_path))
    os.makedirs(generate_config["dial_save_dir"], exist_ok=True)
    return generate_config, gpt_config




def main():
    demo_config, gpt_config = setup_logging_and_config(args)
    
    if args.fake_seed is not None:
        demo_config['dial_save_dir'] = os.path.join(demo_config['dial_save_dir'], f"seed_{args.fake_seed}")
        demo_config['log_path'] = demo_config['log_path'].replace(".log", f"_seed_{args.fake_seed}.log")
        os.makedirs(demo_config['dial_save_dir'], exist_ok=True)
        os.makedirs(os.path.dirname(demo_config['log_path']), exist_ok=True)
        
    logger = Logger(demo_config['log_path'])
    checker = Checker(demo_config['base_model'], demo_config['max_length'])
    ai_client =  AI_CLIENT(demo_config, gpt_config, logger, model_name=args.client_gpt)
    history = History(demo_config, None, logger)
    panic = Panic(demo_config, checker, logger)

    dir_save_path = os.path.join(demo_config["dial_save_dir"], "preference_data.json")
    preference_data = []
    
    
    # 1. Load the data
    if os.path.exists(os.path.join(dir_save_path)):
        with open(dir_save_path, 'r') as f:
            preference_data = json.load(f)
        print(f"Loaded {len(preference_data)} items from existing preference_data at {dir_save_path}")
    else:
        preference_data = []

    # 2. Loop: until args.max_num 
    
    start_time = datetime.now()
    while len(preference_data) < args.max_num:
        cid,_ = ai_client.update_client_info_randomly()
        history.initialize(f'{cid}.json')
        
        data_constructor = Data_Construction(logger, ai_client, history, panic, cid)
        try:
            data_ = data_constructor.get_one_session()
            preference_data.extend(data_)
        except Exception as e:
            logger, print(f"Error occurred: {e}")
            traceback.print_exc()
            import time; time.sleep(5) 
            continue  
        # 3. Save
        with open(dir_save_path, 'w') as f:
            json.dump(preference_data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(preference_data)} dialogues to {dir_save_path}")
        
        logger.log_and_print(f"Collected {len(preference_data)} dialogues so far.")
        mid_time = datetime.now()
        elapsed_time = mid_time - start_time
        elapsed_seconds = elapsed_time.total_seconds()
        elapsed_minutes = elapsed_seconds / 60
        logger.log_and_print(f"Elapsed time: {elapsed_minutes:.2f} minutes")

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    elapsed_seconds = elapsed_time.total_seconds()
    elapsed_minutes = elapsed_seconds / 60
    logger.log_and_print(f"Elapsed time: {elapsed_minutes:.2f} minutes")
    logger.log_and_print("Data collection complete.")
    

   
   
   
   
   
if __name__ == "__main__":
    main()
