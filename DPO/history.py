import json
import os, pdb
class History:
    def __init__(self, config, file_name, logger):
        self.logger = logger
        self.config = config
        self.saving_path = None
        self.update_rule = config["MOVE_RULE"]
        if type(file_name) == str:
            self.saving_path = os.path.join(config["save_path"], file_name)
            
        self.dialogue, self.current_idx = self.set_dialogue(self.saving_path)
        
        
    def initialize(self, file_name = None):
        self.current_idx = ("A", 0)
        self.dialogue = {
            "A": {"plan":"", "dialogue":[]},
            "B": {"plan":"", "dialogue":[]},
            "C": {"plan":"", "dialogue":[]},
        }
        self.saving_path = os.path.join(self.config["dial_save_dir"], file_name)
        
    def set_dialogue(self, previous):
        self.current_idx = ("A", 0)
        dialogue = None
        if type(previous) ==str:
            if os.path.exists(previous):
                self.logger.log_and_print(f"History file found. Loading the file. {previous}")
                dialogue = json.load(open(previous))
        elif type(previous) == dict:
            dialogue = previous
        
        
        if previous is None or dialogue is None:
            self.logger.log_and_print("Nothing found. Creating a new dialogue")
            dialogue ={
                "A": {"plan":"", "dialogue":[]},
                "B": {"plan":"", "dialogue":[]},
                "C": {"plan":"", "dialogue":[]},
            }
            
        if ["A", "B", "C"] == list(dialogue.keys()):
            for part in ["A", "B", "C"]:
                if "plan" in dialogue[part] and len(dialogue[part]["dialogue"]) > 0:
                    self.current_idx = (part, len(dialogue[part]["dialogue"])-1) 
                    
                    
        self.logger.log_and_print(f"Current Index: {self.current_idx}")
        return dialogue, self.current_idx                
                        
                
    def saving(self):
        os.makedirs(os.path.dirname(self.saving_path), exist_ok=True)
        with open(self.saving_path, 'w') as f:
            json.dump(self.dialogue, f, indent=4, ensure_ascii=False)
        
    def history_to_str(self, history_list):
        history_str = ""
        for idx, item in enumerate(history_list):
            # if 'part' in item and 'turn_idx' in item:
                # history_str += f"Part {item['part']} Turn {item['turn_idx']+1}\n"
            if 'system' in item:
                history_str += f"Counselor: {item['system']}\n"
            if 'user' in item:  
                history_str += f"Client: {item['user']}\n"
                    
        return history_str

    def history_for_plan(self):
        part = self.current_idx[0]
        if part == "A":
            history_list = [self.dialogue['A']['dialogue'][0]]
        elif part == "B":
            history_list =  self.dialogue['A']['dialogue']
        elif part == "C":
            history_list = self.dialogue['B']['dialogue']
        else:
            raise ValueError("part should be A, B, or C")
        return history_list
    
        
    def history_for_utt(self): #  history_for_plan_to_utt 와 같음
        part = self.current_idx[0]
        if part == "A":
            dial_list = self.dialogue['A']['dialogue']
        
        elif part == "B":
            if len(self.dialogue['B']['dialogue']) == 0:
                dial_list = [self.dialogue['A']['dialogue'][-1]]
            else:
                dial_list = self.dialogue['B']['dialogue']
        
        elif part == "C":
            if len(self.dialogue['C']['dialogue']) == 0:
                dial_list = [self.dialogue['B']['dialogue'][-1]]
            else:
                dial_list = self.dialogue['C']['dialogue']
            
        else:
            raise ValueError("part should be A, B, or C")
        
        return dial_list
    
    
        
    def note_to_str(self, history_list, part):
        note_return_ = {}

        for item in history_list:
            if 'note' not in item: continue
            for k, v in item['note'].items():
                if v.lower() == '[blank]':
                    continue
                # Replace the existing value with the new one.
                note_return_[k] = v

        # Sort dictionary keys based on `NOTE_KEYS` for the given part and default to '[blank]' if missing.
        sorted_keys = self.config['NOTE_KEYS'].get(part, [])
        sorted_notes = {k: note_return_.get(k, '[blank]') for k in sorted_keys}
        return sorted_notes
            
        
    def update_plan(self, plan, need_save=True):
        self.logger.log_and_print(f"Update the plan: {plan}")
        part = self.current_idx[0]
        self.dialogue[part]["plan"] = plan
        if need_save:
            self.saving()
        
        
    def update_index(self):
        self.current_idx = (self.current_idx[0], self.current_idx[1]+1)
        if self.current_idx[1] >= self.update_rule[self.current_idx[0]]:
            self.logger.log_and_print(f"⏩ Update the part, follow the rule")
            self.update_part()
        
    def update_part(self):
        if self.current_idx[0] == "A":
            part = "B"
        elif self.current_idx[0] == "B":
            part = "C"
        elif self.current_idx[0] == "C":
            part = "END"
        self.current_idx = (part, 0)
        
    def update_dialogue(self,  key, value, need_save):
        if key in ["system", "user"]:
            self.logger.log_and_print(f"Update the dialogue: {key} : {value}")
        part, idx = self.current_idx
        
        if len(self.dialogue[part]["dialogue"]) == idx:
            self.dialogue[part]["dialogue"].append({key: value})
            self.dialogue[part]["dialogue"][idx]["part"] = part
            self.dialogue[part]["dialogue"][idx]["turn_idx"] = idx
        else:
            self.dialogue[part]["dialogue"][idx][key] = value
            
        
        if need_save:
            self.saving()
        