from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.text import Tokenizer # coba langsung panggil dibawah, pake 2.17
from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras.layers import InputLayer
from sklearn.preprocessing import MultiLabelBinarizer
import os

nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)

# Load the pre-trained model
model_file_path = 'model.h5'
# custom_objects = {'Input Layer': InputLayer}
model = tf.keras.models.load_model(model_file_path)

# Load the dataset (for label encoder fitting)
file_path = 'tambahan06.csv'
df = pd.read_csv(file_path)

df1 = df.groupby('title')['sdgs'].apply(lambda x: ','.join(x)).reset_index()

# Assuming text column is 'title' and label is 'sdgs'
texts = df1['title'].astype(str).values
labels = df1['sdgs'].apply(lambda x: x.split(',')).values

# Assuming you have saved MultiLabelBinarizer
mlb = MultiLabelBinarizer()
labels_binarized = mlb.fit_transform(labels)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    return text

texts = [preprocess_text(text) for text in texts]

# Tokenizing and padding sequences
tokenizer = Tokenizer(num_words=20000, oov_token='<OOV>')
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=300, padding='post', truncating='post')

@app.route('/predictsdgs', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded!'}), 500
    
    input_data = request.get_json()
    if input_data is None or 'title' not in input_data:
        return jsonify({'error': 'No input text provided'}), 400

    input_text = input_data['title']
    processed_text = preprocess_text(input_text)
    sequence = tokenizer.texts_to_sequences([processed_text])
    padded_sequence = pad_sequences(sequence, maxlen=300, padding='post', truncating='post')
    prediction = model.predict(padded_sequence)
    predicted_labels = mlb.inverse_transform(prediction > 0.05)
    predicted_labels_list = [label for sublist in predicted_labels for label in sublist]  # Flatten the list
    
    return jsonify({'predicted_labels': predicted_labels_list})

@app.route('/')
def index():
    return 'Welcome to the SDGS Prediction API!'

if __name__ == '__main__':
    app.run(debug=True)