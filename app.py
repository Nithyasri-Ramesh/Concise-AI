import nltk
nltk.download('punkt')
nltk.download('stopwords')
from flask import Flask, request, render_template
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
import string

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('punkt_tab')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def summarix_home():
    if request.method == "POST":
        if "document_text" not in request.form:
            return {"error": "Key must be named 'text'"}, 400

        text = request.form["document_text"]
        
        if not text.strip():
            return {"summary": []}

        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())

        stop_words = set(stopwords.words("english"))
        punctuation = set(string.punctuation)

        filtered_words = [
            word for word in words
            if word not in stop_words and word not in punctuation
        ]

        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1

        if not word_freq:
            return {"summary": []}

        max_freq = max(word_freq.values())
        for word in word_freq:
            word_freq[word] /= max_freq

        sentence_scores = {}
        for sentence in sentences:
            sentence_words = word_tokenize(sentence.lower())
            meaningful_words = [w for w in sentence_words if w in word_freq]

            if len(meaningful_words) < 2: 
                continue

            score = sum(word_freq[w] for w in meaningful_words)
            sentence_scores[sentence] = score / len(meaningful_words)

        best_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
        summary = [s for s in sentences if s in best_sentences]

        return render_template('index.html', summary_points=summary)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
