import numpy as np
import pandas as pd

df = pd.read_csv('https://github.com/davanoraffi/PrediksiSDGS/raw/main/Dataset/tambahan06.csv')

df.info()

df.head()

import re
import string
import nltk
import tensorflow as tf
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional, GlobalMaxPool1D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
import zipfile

df1 = df.groupby('title')['sdgs'].apply(lambda x: ','.join(x)).reset_index()
df1

# Mengecek baris duplikat
duplikat = df1.duplicated()

# Menghitung jumlah total baris duplikat
jumlah_duplikat = duplikat.sum()
print(f"Jumlah total baris duplikat: {jumlah_duplikat}")

from sklearn.preprocessing import MultiLabelBinarizer

# Misalkan kolom teks adalah 'title' dan label adalah 'labels' (labels dalam format list dari string)
texts = df1['title'].astype(str).values
labels = df1['sdgs'].apply(lambda x: x.split(',')).values

# Langkah 3: Binarisasi label untuk multi-label classification
mlb = MultiLabelBinarizer()
labels_binarized = mlb.fit_transform(labels)

# Download NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Langkah 2: Preprocessing teks
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Mengubah teks menjadi huruf kecil
    text = text.lower()
    # Menghapus tanda baca dan angka
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Menghapus stop words dan lemmatization
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    return text

texts = [preprocess_text(text) for text in texts]

# Tokenizing dan padding sequences
tokenizer = Tokenizer(num_words=20000, oov_token='<OOV>')
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=300, padding='post', truncating='post')

# Langkah 4: Membagi data menjadi training dan testing
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels_binarized, test_size=0.2, random_state=42)

#word2vec
word_index = tokenizer.word_index

!wget --no-check-certificate \
     https://nlp.stanford.edu/data/glove.6B.zip \
     -O /content/glove.6B.zip

import zipfile

# Path to the downloaded zip file
zip_path = '/content/glove.6B.zip'

# Path to the extraction directory
extract_path = '/content/glove.6B'

# Extract the zip file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Verify extraction
import os
print(os.listdir(extract_path))

import numpy as np

def load_glove_embeddings(glove_file_path):
    embeddings_index = {}
    with open(glove_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            try:
                coefs = np.asarray(values[1:], dtype='float32')
                embeddings_index[word] = coefs
            except ValueError:
                # Jika ada baris yang tidak bisa dikonversi, lewati baris tersebut
                continue
    return embeddings_index

glove_file_path = '/content/glove.6B/glove.6B.300d.txt'
embeddings_index = load_glove_embeddings(glove_file_path)
print('Found %s word vectors.' % len(embeddings_index))

embedding_matrix = np.zeros((len(word_index) + 1, 300))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

embedding_layer = Embedding(input_dim=len(word_index) + 1,
                            output_dim=300,
                            weights=[embedding_matrix],
                            input_length=300,
                            trainable=False)

from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dropout, Dense, BatchNormalization

model = tf.keras.Sequential([
    embedding_layer,
    Bidirectional(LSTM(512, return_sequences=True)),
    BatchNormalization(),
    Dropout(0.4),
    Bidirectional(LSTM(512)),
    BatchNormalization(),
    Dropout(0.4),
    Dense(512 , activation='relu'),
    Dropout(0.4),
    Dense(len(mlb.classes_), activation='sigmoid')
])

optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

from tensorflow.keras.callbacks import EarlyStopping
from keras.callbacks import ReduceLROnPlateau

# # Early stopping to avoid overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Langkah 6: Melatih model
history = model.fit(X_train, y_train, epochs=25, batch_size=64, validation_split=0.2, callbacks=[early_stopping])

# Langkah 7: Mengevaluasi model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {accuracy}')

# Contoh data baru
new_texts = ["Machine learning in healthcare is revolutionizing the industry",
             "Climate change mitigation strategies and their impacts"]

# Preprocessing teks baru
new_texts_processed = [preprocess_text(text) for text in new_texts]

# Tokenizing dan padding teks baru
new_sequences = tokenizer.texts_to_sequences(new_texts_processed)
new_padded_sequences = pad_sequences(new_sequences, maxlen=300, padding='post', truncating='post')

# Melakukan prediksi
predictions = model.predict(new_padded_sequences)

# Mengubah hasil prediksi menjadi label asli
predicted_labels = mlb.inverse_transform(predictions > 0.05)

# Menampilkan hasil prediksi
for text, labels in zip(new_texts, predicted_labels):
    print(f"Text: {text}")
    print(f"Predicted Labels: {labels}\n")

import pickle
# Save the model in pickle format
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)