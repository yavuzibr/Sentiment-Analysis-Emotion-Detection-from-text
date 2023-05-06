import string
from collections import Counter

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    lowercased_text = text.lower()
    cleaned_text = lowercased_text.translate(str.maketrans('', '', string.punctuation))
    tokenized_words = cleaned_text.split()
    non_emotion_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
                         "yourself",
                         "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                         "itself",
                         "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
                         "that",
                         "these",
                         "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                         "having", "do",
                         "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
                         "while",
                         "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during",
                         "before",
                         "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
                         "under",
                         "again",
                         "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any",
                         "both",
                         "each",
                         "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same",
                         "so",
                         "than",
                         "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    final_words = []
    for word in tokenized_words:
        if word not in non_emotion_words:
            final_words.append(word)

    emotion_list = []
    with open('emotions.txt', 'r') as file:
        for line in file:
            clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
            word, emotion = clear_line.split(':')

            if word in final_words:
                emotion_list.append(emotion)

    emotion_counter = Counter(emotion_list)
    max_value = max(emotion_counter.values())
    max_keys = [key for key, value in emotion_counter.items() if value == max_value]

    if len(max_keys) == 1:
        result = "Emotion of this sentence is " + max_keys[0]
    elif len(max_keys) > 1:
        result = "There are equally h: " + ", ".join(max_keys)
    else:
        result = "The dictionary is empty."

    return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
