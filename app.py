from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
import re
import string
import nltk
# from tensorflow import keras
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.text import Tokenizer # coba langsung panggil dibawah, pake 2.17
from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, BatchNormalization, Dropout, Dense
# from tensorflow.keras.optimizers import Adam
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

### ===== Rebuild Model
# # Recreate the model architecture
# embedding_layer = tf.keras.layers.Embedding(input_dim=20000, output_dim=128, input_length=300)

# model = tf.keras.Sequential([
#     embedding_layer,
#     Bidirectional(LSTM(512, return_sequences=True)),
#     BatchNormalization(),
#     Dropout(0.4),
#     Bidirectional(LSTM(512)),
#     BatchNormalization(),
#     Dropout(0.4),
#     Dense(512, activation='relu'),
#     Dropout(0.4),
#     Dense(num_classes, activation='sigmoid')  # Use the correct number of classes
# ])

# # Compile the model
# optimizer = Adam(learning_rate=0.001)
# model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# # Load the weights from the existing model file
# model.load_weights('model.h5')
### ===== Rebuild Model

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

    print('\n')
    print(f'Predicting "{input_text}"')

    processed_text = preprocess_text(input_text)
    sequence = tokenizer.texts_to_sequences([processed_text])
    padded_sequence = pad_sequences(sequence, maxlen=300, padding='post', truncating='post')
    
    prediction = model.predict(padded_sequence)
    
    print(f'Raw result:\n{prediction}')

    sorted_labels = []
    
    # Take top 3 labels
    for i, pred in enumerate(prediction):
        # Sort prediction probabilities, get the indices of the top 3
        # top_3_indices = np.argsort(pred)[-3:][::-1]
        top_3_indices = [i for i in np.argsort(pred)[::-1] if pred[i] > 0.09][:3]
        top_3_scores = pred[top_3_indices]

        # Get the labels of the top 3 indices
        top_3_labels = tuple([mlb.classes_[index] for index in top_3_indices])
        sorted_labels.append(top_3_labels)

        print(f'Inversed sorted result:\n{str(sorted_labels)}')
        print(f'Scores: {top_3_scores}')
    print('\n')
    


    # predicted_labels = mlb.inverse_transform(prediction > 0.05)
    # predicted_labels_list = [label for sublist in predicted_labels for label in sublist]  # Flatten the list
    predicted_labels_list = [label for sublist in sorted_labels for label in sublist] # try
    
    return jsonify({'predicted_labels': predicted_labels_list})

@app.route('/')
def index():
    return 'Welcome to the SDGS Prediction API!'

if __name__ == '__main__':
    app.run(debug=True)