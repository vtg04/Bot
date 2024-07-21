from flask import Flask, request, jsonify, send_from_directory, session
from sentence_transformers import SentenceTransformer, util
import json
import os

app = Flask(__name__, static_url_path='')
app.secret_key = 'Kyi7'

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("corpus.txt", "r") as file:
    corpus_text = file.read()

with open('Sample Question Answers.json') as f:
    sample_qna = json.load(f)

questions = [qa['question'] for qa in sample_qna]
answers = [qa['answer'] for qa in sample_qna]

questions.append(corpus_text)
answers.append(corpus_text)

question_embeddings = model.encode(questions, convert_to_tensor=True)

def find_best_match(query):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, question_embeddings)[0]
    best_match_idx = scores.argmax().item()
    best_score = scores[best_match_idx].item()
    threshold = 0.5
    if best_score >= threshold:
        return answers[best_match_idx], questions[best_match_idx]
    return None, None

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    conversation_history = session.get('conversation_history', [])
    last_relevant_query = session.get('last_relevant_query', '')

    if user_message.lower() in ["tell me more about it", "tell me more", "more info", "more information"]:
        response = session.get('last_detailed_answer', "Please contact our support for more information.")
        conversation_history.append({'role': 'user', 'content': user_message})
        conversation_history.append({'role': 'bot', 'content': response})
        session['conversation_history'] = conversation_history
        return jsonify({"response": response})
    
    conversation_history.append({'role': 'user', 'content': user_message})
    context = " ".join([message['content'] for message in conversation_history])
    
    brief_response, matched_query = find_best_match(user_message)
    detailed_response, _ = find_best_match(context)
    
    if brief_response:
        conversation_history.append({'role': 'bot', 'content': brief_response})
        session['conversation_history'] = conversation_history
        session['last_relevant_query'] = matched_query
        session['last_detailed_answer'] = detailed_response
        return jsonify({"response": brief_response})
    else:
        fallback_message = "Please contact our support for more information."
        conversation_history.append({'role': 'bot', 'content': fallback_message})
        session['conversation_history'] = conversation_history
        return jsonify({"response": fallback_message})

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
