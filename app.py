from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

DATA_FILE = 'words.txt'
STATE_FILE = 'state.json'

# Load words from the text file
def load_words():
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
    return words

# Save words to the text file
def save_words(words):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        for word in words:
            file.write(f"{word}\n")

# Load state from the JSON file
def load_state():
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as file:
            state = json.load(file)
    except FileNotFoundError:
        state = {}
    return state

# Save state to the JSON file
def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as file:
        json.dump(state, file)

@app.route('/', methods=['GET'])
def index():
    words = load_words()
    state = load_state()
    
    # Combine words and their states into a list of tuples
    word_tuples = [(i, word, state.get(str(i))) for i, word in enumerate(words)]
    
    # Sort by checked status: unchecked first
    word_tuples.sort(key=lambda x: x[2] is not None)
    
    return render_template('index.html', word_tuples=word_tuples)

@app.route('/update_word', methods=['POST'])
def update_word():
    index = int(request.form['index'])
    new_word = request.form['new_word']
    words = load_words()
    words[index] = new_word
    save_words(words)
    return jsonify(success=True)

@app.route('/update_state', methods=['POST'])
def update_state():
    index = int(request.form['index'])
    is_correct = request.form['is_correct']
    state = load_state()
    state[str(index)] = is_correct
    save_state(state)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
