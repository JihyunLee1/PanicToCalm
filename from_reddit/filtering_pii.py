import json
from transformers import pipeline
import pdb
from tqdm import tqdm
gen = pipeline("token-classification", "lakshyakh93/deberta_finetuned_pii")

def has_PII(item):
    
    output = gen(str(item), aggregation_strategy="first")
    # return any([item['entity_group'] == 'PII' for item in output])
    
    pii = [i['entity_group'] for i in output if i['entity_group'] in PII_list]
    
    if pii != [] :
        print(output)
    return len(pii)!=0

PII_list = [
    "EMAIL",
    "BITCOINADDRESS",
    "ETHEREUMADDRESS",
    "ACCOUNTNAME",
    "IBAN",
    "ACCOUNTNUMBER",
    "BIC",
    "IPV4",
    "ZIPCODE",
    "IPV6",
    "CREDITCARDNUMBER",
    "VEHICLEVIN",
    "PASSWORD",
    "PHONE_NUMBER",
    "SSN",
    "LITECOINADDRESS",
    "MAC",
    "CREDITCARDISSUER",
    "CREDITCARDCVV",
    "IP",
    "SEX",
    "PIN",
]


if __name__ == "__main__":
    
    
        # if 'unknown' in [item['catastrophic_thought'].lower(), item['physical_symptom'].lower()]:
        #     return None
        
        
        
    dataset = json.load(open(RAW_REDDIT_PATH))
    new_dataset = {}
    piis = []
    cnt = 0
    for cid, item in tqdm(dataset.items()):
        
        
        try:
            if 'catastrophic_thought' not in item or 'physical_symptom' not in item:
                continue
            if 'unknown' in [item['catastrophic_thought'].lower(), item['physical_symptom'].lower()]:
                continue
        except:
            continue
        
        cnt +=1 
        if has_PII(item):
            continue
        

        
        new_dataset[cid] = item
        
        
    json.dump(new_dataset, open(SAVEPATH, "w"), indent=4)
    
    json.dump(piis, open("piis.json", "w"), indent=4)
    
    print("new : ", len(new_dataset), "original : ", cnt)


# 1443, 1452, 3149
    







