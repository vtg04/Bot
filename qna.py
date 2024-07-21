import json

with open('Sample Question Answers.json') as f:
    sample_qna = json.load(f)

print(sample_qna)