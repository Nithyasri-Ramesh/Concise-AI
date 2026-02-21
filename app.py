from flask import Flask, render_template, request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
import os

app = Flask(__name__)

# --- VERCEL SPECIFIC NLTK SETUP ---
# Vercel is read-only, so we must download NLTK data to /tmp
nltk_data_dir = "/tmp/nltk_data"
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

# Download necessary NLTK packages
nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir)
# ----------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    article_text = request.form['text']
    
    # Text Cleaning
    stop_words = set(stopwords.words('english'))
    word_frequencies = {}
    for word in word_tokenize(article_text):
        if word.lower() not in stop_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Weighted Frequencies
    if not word_frequencies:
        return render_template('index.html', summary="Please enter valid text.")
        
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    # Sentence Scores
    sentence_list = sent_tokenize(article_text)
    sentence_scores = {}
    for sent in sentence_list:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    # Pick top 3 sentences
    summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    
    return render_template('index.html', summary=summary, original_text=article_text)

if __name__ == '__main__':
    app.run(debug=True)