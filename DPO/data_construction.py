from history import History
import random
import pdb
import os, json
# format should be
'''
{
  "prompt": "Client: I feel like I can't breathe. Everything is closing in on me.\nCounselor:",
  "chosen": "You're not alone right now. Can you find somewhere to sit and take a deep breath with me?",
  "rejected": "Please calm down. You’ll be fine eventually, it’s just stress."
}
'''

# (logger, ai_client, history, panic)
class Data_Construction:
    def __init__(self, logger, client_api, history_api, panic_api, cid = None):
        self.logger = logger
        self.client_api = client_api
        self.history_api = history_api
        self.panic_api = panic_api
        self.cid = cid
        
        
    def get_best_and_worst_move(self, client, move_to_next, history, compare_num = 2):
        if len(set(move_to_next)) == 1: # 다 같으면 best,worst없음
            return [0], [], '', ''
        else:
            result, reason = client.ask_move_to_next(history) # result : move_to_next or keep_this_stage
            best, worst = [], []
            for idx, v in enumerate(move_to_next):
                if v == result:
                    best.append(idx)
                else:
                    worst.append(idx)
            best = best[:compare_num]
            worst = worst[:compare_num]
            return best, worst, result, reason
        
    def get_best_and_worst_utt(self, client, utts, history, min_diff = 1):
        best_idx, worst_idx, diff = None, None, None
        result = client.ask_eval_utt(utts, history) # result : move_to_next or keep_this_stage # {index: {score, reason}}
        
        best = sorted(result.items(), key=lambda x: x[1]['score'], reverse=True)[0] #(idx, scoring) tuples comes out
        worst = sorted(result.items(), key=lambda x: x[1]['score'])[0]
        diff = float(best[1]['score']) - float(worst[1]['score'])
        if diff >= min_diff:
            best_idx = int(best[0].replace("idx",""))
            worst_idx = int(worst[0].replace("idx",""))

        return best_idx, worst_idx, diff, result
    
    
    def get_best_and_worst_format(self, output, compare_num = 2):
        best_list, worst_list = [], [] # TODO
        best_list = output['original_output'][:compare_num] 
        worst_list = output['errors'][:compare_num]
        return best_list, worst_list


    def make_dpo_data(self, org_input, generated_texts, m_best_idx, m_worst_idx, data_type):
        data = [] 
        if type(m_best_idx) == int:
            m_best_idx = [m_best_idx]
        if type(m_worst_idx) == int:
            m_worst_idx = [m_worst_idx]
            
        for i in range(len(m_best_idx)):
            for j in range(len(m_worst_idx)):
                if m_best_idx[i] == m_worst_idx[j]: continue
                data.append({
                    "prompt": org_input,
                    "chosen": 'assistant\n\n' + generated_texts[m_best_idx[i]] + ' [END]',
                    "rejected": 'assistant\n\n' + generated_texts[m_worst_idx[j]] + ' [END]',
                    "cid": self.cid,
                    "data_type": data_type,
                })
        return data
    
    
    def set_dpo_policy(self, counselor_output, history):
        type_of_move = len(set(counselor_output['move_to_nexts'])) # 1: move, 2: keep_this_stage
        DPO_FOR_REASONING = type_of_move != 1
        DPO_FOR_UTT = type_of_move ==1 and counselor_output['move_to_nexts'][0] == False and history.current_idx != ("A", 0)
        # If the part is C, don't reasoning
        if history.current_idx[0] == "C":
            DPO_FOR_REASONING = False 
        assert not (DPO_FOR_REASONING and DPO_FOR_UTT), "DPO_for_reasoning and DPO_for_utt are not compatible"
        
        DPO_FOR_FORMAT = False if len(counselor_output['errors']) == 0 else True
        return DPO_FOR_REASONING, DPO_FOR_UTT, DPO_FOR_FORMAT
            
    def set_move_policy(self, counselor_output, history, client_opinion ):
        type_of_move = len(set(counselor_output['move_to_nexts']))
        if type_of_move == 1 and counselor_output['move_to_nexts'][0] == True:
            return True
        elif history.current_idx[0] !="C" and client_opinion and True in counselor_output['move_to_nexts']:
            return True
        elif history.current_idx[0] == "C" and counselor_output['move_to_nexts'][0] == True:
            return True
        else:
            return False
            
    def get_one_session(self):
        data = []
        client, history = self.client_api, self.history_api

        while history.current_idx != ('END', 0):
            counselor_output = self.panic_api.chat(history, k=10)
            self._update_plan_if_available(counselor_output, history)
            
            ### 1. Process the reasoning part ####
            DPO_FOR_REASONING, DPO_FOR_UTT, DPO_FOR_FORMAT = self.set_dpo_policy(counselor_output,history)
            best_idx_rsn = None
            if DPO_FOR_REASONING:
                move_best_idx, move_worst_idx, mv_client_opinion, mv_client_reason = self.get_best_and_worst_move(
                    client, counselor_output['move_to_nexts'], history, compare_num = 2
                )
                if mv_client_opinion == False: data_type = "move_client_false"
                elif mv_client_opinion == True: data_type = "move_client_true" # DO Nothing in this case
                data.extend(self._make_dpo_from_idx(counselor_output, move_best_idx, move_worst_idx, data_type = data_type))
    
                best_idx_rsn = move_best_idx[0]
            else:
                mv_client_opinion, mv_client_reason= False, 'not performed'
                
            history.update_dialogue("client_want move", mv_client_opinion, need_save=True)
            history.update_dialogue("client_want move_reason", mv_client_reason, need_save=True)
            
            MOVE_THE_PART = self.set_move_policy(counselor_output, history, mv_client_opinion)
            if MOVE_THE_PART:
                history.update_part()
                continue
            
            ### 2. Process the utterance part ####
            
            best_idx_utt = 0 
            if DPO_FOR_UTT:
                best_idx_utt, worst_idx_utt, diff, all_result = self.get_best_and_worst_utt(
                    client, counselor_output['system_utts'], history)
                if best_idx_utt !=None:
                    history.update_dialogue("client_eval", {"diff" : diff, "best": counselor_output['system_utts'][best_idx_utt], "worst" : counselor_output['system_utts'][worst_idx_utt]}, need_save=True)
                    history.update_dialogue("client_full", all_result, need_save=True)
                    
                    data.extend(self._make_dpo_from_idx(counselor_output, best_idx_utt, worst_idx_utt, data_type = "utt"))
                    self.logger.log_and_print(f"\n❤ Best response: {counselor_output['system_utts'][best_idx_utt]}")
                    self.logger.log_and_print(f"💔 Worst response: {counselor_output['system_utts'][worst_idx_utt]}\n")
                else:
                    best_idx_utt = 0
                
            ### 3. Process the format part ####
            if DPO_FOR_FORMAT:
                best_list, worst_list = self.get_best_and_worst_format(counselor_output)
                if len(best_list) > 0 and len(worst_list) > 0:
                    data.extend(self._make_dpo_from_list(counselor_output, best_list, worst_list, data_type = "format"))
                    self.logger.log_and_print(f"\n❤ Format Best response: {best_list[0]}")
                    self.logger.log_and_print(f"💔 Format Worst response: {worst_list[0]}\n")

            best_idx = best_idx_rsn if best_idx_rsn != None else best_idx_utt # rsn first, then utt
            
            system_utt = counselor_output['system_utts'][best_idx]
            rsn = counselor_output['rsns'][best_idx]
            self._update_history_with_system(history, counselor_output, rsn, system_utt)


            ### 4. Process the user part ####
            user_utt = client.chat(history)
            history.update_dialogue("user", user_utt, need_save=True)
            history.update_index()

        return data
        
    def _update_plan_if_available(self, output, history):
        if output['plan']:
            history.update_plan(output['plan'], need_save=True)

    def _make_dpo_from_idx(self, output, best_idx, worst_idx, data_type):
        return self.make_dpo_data(
            output['original_input'],
            output['original_output'],
            best_idx,
            worst_idx,
            data_type
        )


    def _make_dpo_from_list(self, output, best_list, worst_list, data_type):
        # need to calculate the best and worst index from the list
        best_idx, worst_idx = [], [] # TODO
        
        inputs = best_list + worst_list
        for i in range(len(inputs)):
            if inputs[i] in best_list:
                best_idx.append(i)
            else:
                worst_idx.append(i)
                
                
        return self.make_dpo_data(
            output['original_input'],
            output['original_output'],
            best_idx,
            worst_idx,
            data_type
        )
        
        
    def _update_history_with_system(self, history, output, rsn, utt):
        history.update_dialogue("reasoning", rsn, need_save=True)
        history.update_dialogue("reasoning_candidates", output['rsns'], need_save=True)
        history.update_dialogue("system", utt, need_save=True)
        history.update_dialogue("system_candidates", output['system_utts'], need_save=True)