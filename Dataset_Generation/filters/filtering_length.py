# simple format filetring

import argparse
import json
import pdb
import random



A_TURN_MAX = 20
B_TURN_MAX = 20
C_TURN_MAX = 10

A_SYS_MAX = 100
B_SYS_MAX = 100
C_SYS_MAX = 100





def part_lengths(data):
    parts = ['A', 'B', 'C']
    lengths = {}
    
    for part in parts:
        part_data  = data[part]
        lengths[part] = len(part_data['dialogue'])
        
    if lengths['A'] > A_TURN_MAX or lengths['B'] > B_TURN_MAX or lengths['C'] > C_TURN_MAX:
        return False
    return True

def utt_lengths(data):
    iteration = [(data['A'], A_SYS_MAX), (data['B'], B_SYS_MAX), (data['C'], C_SYS_MAX)]
    
    for part, max_len in iteration:
        for turn in part['dialogue']:
            if len(turn['system'].split()) > max_len:
                return False
            
            
    return True


def length_filtering(item):
    return part_lengths(item) and utt_lengths(item)


if __name__ == "__main__":
    pass