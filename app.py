from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import nltk
nltk.download('punkt')

app = Flask(__name__)

# Load the model
model = load_model('sentiment_model.h5')

# Load the tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Function to analyze sentiment
def analyze_sentiment(text):
    negative_text = ''
    count = 0
    paragraphs = text.split('\n\n')
    for paragraph in paragraphs:
        sentences = nltk.tokenize.sent_tokenize(paragraph)
        for sentence in sentences:
            sequence = tokenizer.texts_to_sequences([sentence])
            padded_sequence = pad_sequences(sequence, maxlen=100)
            prediction = model.predict(padded_sequence)[0][0]
            if prediction >= 0.5:
                count += 1
                negative_text += f'<span class="negative-sentence">{sentence}</span> '
            else:
                negative_text += sentence + ' '
            negative_text += '<br><br>'
        negative_text += '<br>'
    return negative_text, count

@app.route('/', methods=['GET', 'POST'])
def index():
    dark_mode = request.cookies.get('dark_mode', '')
    if request.method == 'POST':
        text = request.form['text']
        negative_text, count = analyze_sentiment(text)
        return render_template('index.html', negative_text=negative_text, count=count, dark_mode=dark_mode)
    return render_template('index.html', dark_mode=dark_mode)

# if __name__ == '__main__':
#     app.run(debug=True)
