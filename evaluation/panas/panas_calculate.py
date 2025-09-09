# Reference: Code implementation inspired by
# https://github.com/coding-groot/cactus

import os
import pdb
import json
from collections import defaultdict

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--before_file", type=str, required=True)
parser.add_argument("--after_file", type=str, required=True)
parser.add_argument("--save_path", type=str, required=True)


def save_file(args, avg_score_dict):
    with open(args.save_path, 'w') as json_file:
        json.dump(avg_score_dict, json_file, indent=4)
    print("Saved the file to", args.save_path)

CRITERIA_LIST = [
    "Interested", "Excited", "Strong", "Enthusiastic", "Proud",
    "Alert", "Inspired", "Determined", "Attentive", "Active",
    "Distressed", "Upset", "Guilty", "Scared", "Hostile",
    "Irritable", "Ashamed", "Nervous", "Jittery", "Afraid"
]

def load_score_data(filepath, is_before=True):
    """JSON 파일을 열고 감정 점수를 딕셔너리로 파싱"""
    with open(filepath, 'r') as f:
        data = json.load(f)

    parsed_data = {}

    for key, value in data.items():
        # after 파일의 경우 key 정리 필요
        cleaned_key = '_'.join(key.split('_')[2:]) if not is_before and 'client' in key else key
        try:
            parsed_data[cleaned_key] = {emotion: int(info['score']) for emotion, info in value.items()}
        except Exception as e:
            print(f"Error parsing {'before' if is_before else 'after'} data for key: {key} — {e}")
    
    return parsed_data

def analyze_score_difference(before_scores, after_scores, client_info=None):
    """Before/After 점수 차이 분석 및 긍정/부정 평균 변화 계산"""
    score_diff = defaultdict(int)
    if client_info:
        score_diff = {'physical':defaultdict(list),
                      'emotional':defaultdict(list),
                      'unknown':defaultdict(list)  ,
                      'environmental':defaultdict(list) } 

    # 점수 차이 누적
    for client_id in after_scores:
        if client_id not in before_scores:
            print(f"Missing client in before data: {client_id}")
            continue
        if client_info:
            client_type = client_info[client_id]['trigger_type']
        for emotion in after_scores[client_id]:
            before = before_scores[client_id].get(emotion, 0)
            after = after_scores[client_id].get(emotion, 0)
            if client_info:              
                score_diff[client_type][emotion].append(after - before)
            else:
                score_diff[emotion] += (after - before)
                
                
    num_clients = len(after_scores)

    if client_info:
        # 감정 점수 차이 평균
        for client_type in score_diff:
            for emotion in score_diff[client_type]:
                score_diff[client_type][emotion] = round(sum(score_diff[client_type][emotion]) / len(score_diff[client_type][emotion]),2)
    else:
        score_diff = {emotion: round(diff /num_clients,2) for emotion, diff in score_diff.items()}

    # 긍정/부정 감정 평균 변화
    
    if client_info:
        for client_type in score_diff:
            score_diff[client_type]["positive_diff"] = round(sum(score_diff[client_type][e] for e in CRITERIA_LIST[:10]) /10,2)
            score_diff[client_type]["negative_diff"] = round(sum(score_diff[client_type][e] for e in CRITERIA_LIST[10:]) /10,2)
    
    else:
        score_diff["positive_diff"] = round(sum(score_diff[e] for e in CRITERIA_LIST[:10]) /10,2)
        score_diff["negative_diff"] = round(sum(score_diff[e] for e in CRITERIA_LIST[10:]) /10,2)

    return score_diff
def save_file(args, result_dict):
    """결과 저장"""
    os.makedirs(os.path.dirname(args.save_path), exist_ok=True)
    with open(args.save_path, 'w') as f:
        json.dump(result_dict, f, indent=2)
    print(f"Saved score analysis to {args.save_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before_file", type=str, required=True)
    parser.add_argument("--after_file", type=str, required=True)
    parser.add_argument("--save_path", type=str, required=True)
    parser.add_argument("--client_path", type=str) # client profile
    args = parser.parse_args()

    
    before_scores = load_score_data(args.before_file, is_before=True)
    after_scores = load_score_data(args.after_file, is_before=False)

    client_info = json.load(open(args.client_path, 'r'))
    score_diff = analyze_score_difference(before_scores, after_scores)
    score_diff_sep = analyze_score_difference(before_scores, after_scores, client_info)
    
    for panic_type in [ 'environmental',  'emotional', 'physical', 'unknown']:
        score_diff[f'{panic_type}_positive'] = score_diff_sep[panic_type]['positive_diff']
        score_diff[f'{panic_type}_negative'] = score_diff_sep[panic_type]['negative_diff']
    save_file(args, score_diff)
    print("Score analysis completed.")

if __name__ == "__main__":
    main()