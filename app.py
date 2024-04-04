import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
import pickle
import nltk

# Load the dataset
file_path = 'combined_data.xlsx'
data = pd.read_excel(file_path)
data.replace({-1: 0, 1: 1}, inplace=True)
data['overall_sentiment'] = data.drop(columns=['sentence']).apply(lambda row: 1 if row.sum() > 0 else 0, axis=1)

# Initialize tokenizer and fit on sentences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['sentence'])

# Convert sentences to sequences and pad them
sequences = tokenizer.texts_to_sequences(data['sentence'])
X = pad_sequences(sequences)
y = data['overall_sentiment'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the model
vocab_size = len(tokenizer.word_index) + 1
max_length = X.shape[1]
model = Sequential([
    Embedding(vocab_size, 16),
    GlobalAveragePooling1D(),
    Dense(24, activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))

# Function to analyze sentiment
def analyze_sentiment(text):
    negative_text = ''
    count = 0
    paragraphs = text.split('\n\n')
    for paragraph in paragraphs:
        sentences = nltk.tokenize.sent_tokenize(paragraph)
        for sentence in sentences:
            sequence = tokenizer.texts_to_sequences([sentence])
            padded_sequence = pad_sequences(sequence, maxlen=max_length)
            prediction = model.predict(padded_sequence)[0][0]
            if prediction >= 0.5:
                count += 1
                negative_text += f'<span class="negative-sentence">{sentence}</span> '
            else:
                negative_text += sentence + ' '
            negative_text += '<br><br>'
        negative_text += '<br>'
    return negative_text, count

# Flask app
from flask import Flask, request, render_template_string
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    dark_mode = request.cookies.get('dark_mode', '')
    if request.method == 'POST':
        text = request.form['text']
        negative_text, count = analyze_sentiment(text)
        return render_template_string(html_template, negative_text=negative_text, count=count, dark_mode=dark_mode)
    return render_template_string(html_template, dark_mode=dark_mode)

html_template = """
<!DOCTYPE html>
<html>
  <head>
    <title>Unfair Clause Analyzer</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        {% if dark_mode %}
        background-color: #222;
        color: #ddd;
        {% else %}
        background-color: #222;
        color: #333;
        {% endif %}
        padding: 20px;
      }
      h1 {
        color: #45a049;
        text-align: center;
      }
      form {
        max-width: 600px;
        margin: 0 auto;
        background-color: {% if dark_mode %} #333 {% else %} #fff {% endif %};
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      }
      textarea {
        width: calc(100% - 22px);
        height: 150px;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
      }
      input[type=submit] {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
      }
      input[type=submit]:hover {
        background-color: #45a049;
      }
      .result {
        max-width: 600px;
        margin: 20px auto 0;
        background-color: {% if dark_mode %} #333 {% else %} #fff {% endif %};
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        color: {% if dark_mode %} #ddd {% else %} #333 {% endif %};
      }
      .negative-sentence {
        color: red;
      }
      .bottom-border {
        position: fixed;
        bottom: 0;
        left: 0;
        width: calc(100% - 50px);
        background-color: #333;
        padding: 1px 20px;
        text-align: center;
        font-size: 12px;
        border-top: 1px solid #ccc;
        border-bottom-left-radius: 1px;
        border-bottom-right-radius: 1px;
      }
      .disclaimer {
        font-size: 13px;
        color: #999;
        margin-top: 0.1px;
        margin-bottom: 0.1px;
      }
    </style>
  </head>
  <body>
    <h1>Unfair Clause Analyzer</h1>
    <form method="post">
      <label for="text">Enter text:</label><br>
      <textarea name="text" rows="5" cols="50"></textarea><br>
      <input type="submit" value="Analyze">
    </form>
    {% if negative_text %}
    <div class="result">
      <p><strong>Total number of negative sentences: {{ count }} {% if count == 0 %}😊{% elif count < 5 %}😐{% else %}😡{% endif %}</strong></p>
      <p>{{ negative_text|safe }}</p>
    </div>
    {% endif %}
    <div class="bottom-border">
      <p class="disclaimer">Disclaimer: Unfair clause analyzer can make mistakes. Take a moment to verify pertinent information.</p>
    </div>
  </body>
</html>
"""

if __name__ == '__main__':
    app.run(port=5000)
