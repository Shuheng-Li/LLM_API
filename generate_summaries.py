from vllm import LLM, SamplingParams
import os, csv, pickle, json

def llama_add_chat_template(prompt):
    return f"[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n\n{prompt} [/INST]"

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

with open('datasets/long_stories.txt', 'r') as f:
    stories = f.readlines()


repeated_stories = [story for story in stories for _ in range(5)]
repeated_prompts = [llama_add_chat_template(story + "\n\nSummarize the above in one sentence.") for story in repeated_stories]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=200)

llm = LLM(model="/data/models/hf/Llama-2-7b-chat-hf")

outputs = llm.generate(repeated_prompts, sampling_params=sampling_params)


output_file_path = 'datasets/long_story_and_summaries_7b.csv'

# Write to the CSV file
with open(output_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['story', 'summary'])  # Writing header row, if needed
    
    for item1, item2 in zip(repeated_stories, [output.outputs[0].text.replace("\n", "") for output in outputs]):
        writer.writerow([item1, item2])