import jsonlines
import pdb
import base64
import os
import requests
import json
from openai import OpenAI
import time
from tqdm import tqdm



def process_live(payloads, is_json = True):
    
    results = {}
    for payload in tqdm(payloads):
        predicted_review=openai_predict(payload['body'], os.environ["OPENAI_API_KEY"])
        if is_json:
            try:
                formatted_review = to_json(predicted_review)  
            except:
                print("Error in processing the payload")
                formatted_review = predicted_review
        else:
            formatted_review = predicted_review
            
        results[payload['custom_id']] = formatted_review
        print(f"Processed {payload['custom_id']}")
        print(f"Result: {formatted_review}")
    return results



def split_jsonl_file(input_file, max_lines=100):
    """
    Splits a large JSONL file into multiple smaller files, each with at most `max_lines` lines.

    Parameters:
        input_file (str): Path to the original JSONL file.
        max_lines (int): Maximum number of lines per split file.

    Returns:
        list: A list of paths to the split files.
    """
    split_files = []
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) <= max_lines:
        return [input_file]  # No need to split if under the limit

    base_name = os.path.splitext(input_file)[0]  # Extract filename without extension
    for i in range(0, len(lines), max_lines):
        split_filename = f"{base_name}_part{i//max_lines}.jsonl"
        with open(split_filename, "w", encoding="utf-8") as f:
            f.writelines(lines[i:i + max_lines])
        split_files.append(split_filename)

    return split_files

def concatenate_jsonl_files(file_list, output_file):
    """
    Concatenates multiple JSONL files into a single file.

    Parameters:
        file_list (list): List of file paths to concatenate.
        output_file (str): Path to the final output file.
    """
    with open(output_file, "w", encoding="utf-8") as outfile:
        for file in file_list:
            with open(file, "r", encoding="utf-8") as infile:
                outfile.writelines(infile.readlines())

def process_batch(save_temp, save_result, is_json = True):
    client = OpenAI()
    split_files = split_jsonl_file(save_temp, max_lines=1000)
    temp_results = []

    for file in split_files:
        print(f"Processing batch for {file}...")
        
        # Upload batch file
        batch_input_file = client.files.create(
            file=open(file, "rb"),
            purpose="batch"
        )
        batch_input_file_id = batch_input_file.id

        # Create batch process
        obj = client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={"description": "nightly eval job"}
        )
        obj_id = obj.id

        # Wait for batch to complete
        while True:
            retrieved = client.batches.retrieve(obj_id)
            if retrieved.status in ['completed', 'expired', 'cancelling', 'cancelled', 'failed']:
                break
            print("status: ", retrieved.status)
            if retrieved.status == 'in_progress':
                print(retrieved.request_counts)
            time.sleep(10)
            print("Waiting for 10 seconds\n")

        if retrieved.status == 'failed':
            print(f"Batch failed for {file}")
            print("Error message:", client.batches.retrieve(obj_id).errors.data[0].message)

        elif retrieved.status == 'completed':
            output_content = client.files.content(retrieved.output_file_id).content
            temp_result_file = f"{file}_result.jsonl"
            with open(temp_result_file, "w", encoding="utf-8") as f:
                f.write(output_content.decode('utf-8'))
            temp_results.append(temp_result_file)

    # Concatenate results
    if temp_results:
        concatenate_jsonl_files(temp_results, save_result)

    # Cleanup temp files except the original one
    for file in split_files:
        if file != save_temp:
            os.remove(file)
    for temp_result in temp_results:
        os.remove(temp_result)

    print(f"Final result saved in {save_result}")
    batch_processed = parsing_batch_result(save_result, is_json=is_json)
    return batch_processed
        
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
    
def openai_predict(payload, key, use_img=1):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
    }
            
            
    response = requests.post("https://api.openai.com/v1/chat/completions",headers=headers, json=payload).json()
    try:
        result =  response['choices'][0]['message']['content']
    except:
        print(response)
        exit()
    return result



def make_line(custom_id, prompt, image_path=None, model_name ="gpt-4o", max_tokens = 5012):
    
    if image_path:
        base64_image = encode_image(image_path)
        image_content = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": "low"
            }
        }
    
    text_content = {
        "type": "text",
        "text": prompt
    }
    content = [text_content]
    
    if image_path:
        content = [text_content, image_content]
    else:
        content = [text_content]    
        
    payload = {
    "model": model_name,
    "messages": [
        {
        "role": "user",
        "content": content
        }
    ],
    "max_tokens": max_tokens
    }
    
    overall = {
        'custom_id' : custom_id,
        'method' : 'POST',
        'url' : '/v1/chat/completions',
        'body' : payload,
    }
    return overall


def parsing_batch_result(file_path, is_json):
    # Dictionary to store the parsed data
    data = {}

    # Read jsonl file
    with jsonlines.open(file_path) as reader:
        for line in reader:
            try:
                custom_id = line["custom_id"]
                response_text = line['response']['body']['choices'][0]['message']['content']
                
                if is_json:
                    try:
                        response_data = to_json(response_text)
                    except json.JSONDecodeError:
                        print(f"Warning: Could not parse JSON for custom_id: {custom_id}")
                        response_data = response_text  # Fallback to raw text if parsing fails

                    data[custom_id] = response_data
                else:
                    data[custom_id] = response_text
            except Exception as e:
                print(f"Error processing line: {e}")
                continue

    return data




