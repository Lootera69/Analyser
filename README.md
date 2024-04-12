# Clause Analyzer

## Introduction
Clause Analyzer is a web application designed to analyze terms and conditions for unfair clauses. It utilizes natural language processing techniques to identify potentially unfair or biased sentences within legal documents.

### Features
- **Sentiment Analysis**: The application employs machine learning models to perform sentiment analysis on input text, flagging negative sentences for further review.
- **User-friendly Interface**: With a clean and intuitive interface, users can easily paste terms and conditions for analysis and receive instant feedback.
- **Word Limit**: The analyzer imposes a word limit of 10,000 words to ensure efficient processing and accurate results.
- **Feedback Mechanism**: Users can provide feedback on the application directly via email, enabling continuous improvement.

## Setup and Usage
1. **Installation**: Clone the repository and install the required dependencies using `pip install -r requirements.txt`.
2. **Running the Application**: Execute `python app.py` to start the Flask web server.
3. **Accessing the Application**: 
    - You can access the application locally by opening a web browser and navigating to `http://localhost:5000`.
    - Alternatively, you can access the hosted version of the application on [Render](https://analyser-bztv.onrender.com/).


## Components
### 1. `train_model.py`
This Python script is responsible for training the sentiment analysis model using a dataset of labeled sentences. It utilizes the TensorFlow and scikit-learn libraries for data preprocessing and model training.

    - **Load Dataset**: The script loads the dataset containing labeled sentences from an Excel file.
    - **Preprocess Data**: It preprocesses the data, replacing labels (-1, 1) with (0, 1) and generating an overall sentiment label for each sentence.
    - **Tokenization**: The tokenizer is initialized and fit on the sentences in the dataset.
    - **Model Training**: A neural network model is built using TensorFlow, consisting of an embedding layer, a pooling layer, and dense layers. The model is trained on the preprocessed data.
    - **Save Model**: Once trained, the model is saved to a file for later use.
    - **Save Tokenizer**: The trained tokenizer is also saved to a file using pickle for future text preprocessing.

### 2. `app.py`
The Flask application serves as the backend for the web interface. It loads the trained sentiment analysis model and tokenizer, allowing users to input text for analysis. The application provides real-time feedback on potentially negative clauses.

    - **Initialize Model and Tokenizer**: The application initializes the sentiment analysis model and tokenizer when it starts.
    - **Analyze Sentiment**: Upon receiving user input, the application tokenizes the text, performs sentiment analysis using the loaded model, and highlights negative clauses.
    - **Handle User Interaction**: It handles user interactions by serving HTML templates and processing form submissions.
    - **Feedback Mechanism**: Users can provide feedback on the analysis process via the provided email link, facilitating continuous improvement.

### 3. `index.html`
The HTML template defines the structure and layout of the web interface. It includes form elements for user input, dynamic updating of word count, and display of analysis results. Additionally, it integrates CSS styles for a visually appealing user experience.

    - **Form Submission**: Users can input terms and conditions into a text area and submit them for analysis.
    - **Word Count**: The interface dynamically updates the word count as users type, ensuring they stay within the 10,000-word limit.
    - **Visual Feedback**: Upon analysis completion, negative sentences are highlighted, providing users with clear feedback on potentially unfair clauses.

## Usage Instructions
1. **Input Text**: Paste the terms and conditions into the text area provided on the web interface.
2. **Analyze**: Click the "Analyze" button to initiate the sentiment analysis process.
3. **Review Results**: The application will display the total number of negative sentences detected, along with highlighted negative clauses for review.
4. **Feedback**: Users can provide feedback on the analysis process via the provided email link.

## Disclaimer
Clause Analyzer is a tool designed to assist in identifying potentially unfair clauses within legal documents. However, it may not be exhaustive or error-free. Users are encouraged to verify critical information independently.

## Contributing
Contributions to the project are welcome! Feel free to submit bug reports, feature requests, or pull requests via GitHub.

## Credits
- Developed by Chetan Harshit Singh
- Icons sourced from [Icon Source]
- Background video sourced from [Video Source]

## License
This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.
