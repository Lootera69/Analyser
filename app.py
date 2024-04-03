# Install required packages
# !pip install flask

# Import necessary libraries
from flask import Flask, request, render_template_string
import pickle
from tensorflow.keras.models import load_model
import nltk
from keras.preprocessing.sequence import pad_sequences

# Download the required NLTK data
nltk.download('punkt')

# Load the saved model and tokenizer
model = load_model('sentiment_model.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Create Flask app
app = Flask(__name__)

# Define the route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    dark_mode = request.cookies.get('dark_mode', '')
    if request.method == 'POST':
        text = request.form['text']
        negative_text, count = analyze_sentiment(text)
        return render_template_string(html_template, negative_text=negative_text, count=count, dark_mode=dark_mode)
    return render_template_string(html_template, dark_mode=dark_mode)

# Function to analyze sentiment
def analyze_sentiment(text):
    negative_text = ''
    count = 0
    paragraphs = text.split('\n\n')  # Split text into paragraphs
    for paragraph in paragraphs:
        sentences = nltk.tokenize.sent_tokenize(paragraph)
        for sentence in sentences:
            sequence = tokenizer.texts_to_sequences([sentence])
            padded_sequence = pad_sequences(sequence, maxlen=X.shape[1])
            prediction = model.predict(padded_sequence)[0][0]
            if prediction >= 0.5:
                count += 1
                negative_text += f'<span class="negative-sentence">{sentence}</span> '
            else:
                negative_text += sentence + ' '
            negative_text += '<br><br>'  # Add <br> after each sentence
        negative_text += '<br>'  # Add <br> between paragraphs
    return negative_text, count


# HTML template
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
        width: calc(100% - 22px); /* Adjusted width to account for border */
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
      /* Border style */
      .bottom-border {
        position: fixed;
        bottom: 0;
        left: 0;
        width: calc(100% - 50px); /* Adjusted width to account for padding */
        background-color: #333; /* Adjust background color as needed */
        padding: 1px 20px; /* Smaller padding */
        text-align: center;
        font-size: 12px;
        border-top: 1px solid #ccc; /* Adjust border color and thickness as needed */
        border-bottom-left-radius: 1px;
        border-bottom-right-radius: 1px;
      }
      .disclaimer {
        font-size: 13px; /* Smaller font size */
        color: #999;
        margin-top: 0.1px; /* Smaller margin */
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
    <!-- Disclaimer -->
    <div class="bottom-border">
      <p class="disclaimer">Disclaimer: Unfair clause analyzer can make mistakes. Take a moment to verify pertinent information.</p>
    </div>
  </body>
</html>

"""


# Run the Flask app
if __name__ == '__main__':

    from google.colab.output import eval_js
    # print(eval_js("google.colab.kernel.proxyPort(5000)"))
    app.run()(debug=False,host='0.0.0.0')