import os
from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google.cloud import language_v1
import json
import sys
import requests
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from mycrawler.text_search.semantic_search import search as semantic_search

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/karishmamajeeth/PycharmProjects/Advanced-Semantic-Search-System /mycrawler/mycrawler/credentials/firm-progress-421117-5399a658e4fd.json"

app = Flask(__name__)

client = language_v1.LanguageServiceClient()

# Load the documents
with open('/Users/karishmamajeeth/PycharmProjects/Advanced-Semantic-Search-System /mycrawler/mycrawler/arxiv_papers.json') as f:
    documents = json.load(f)
contents = [doc['abstract'] for doc in documents if 'abstract' in doc]

# Initialize the semantic search indexer
indexer = semantic_search('/Users/karishmamajeeth/PycharmProjects/Advanced-Semantic-Search-System/mycrawler/mycrawler/arxiv_papers.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search_endpoint():
    if request.method == 'POST':
        app.logger.debug("Received POST request: %s", request.json)
        query = request.json.get('query')
        if not query:
            app.logger.error("No query provided")
            return jsonify({'error': 'No query provided'}), 400

        # Compute cosine similarity
        vectorizer = TfidfVectorizer(stop_words=None)
        tfidf_matrix = vectorizer.fit_transform(contents)
        query_vec = vectorizer.transform([query])
        cos_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

        # Collect top similar documents with their scores
        results = [(idx, score) for idx, score in enumerate(cos_similarities)]
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        top_results = sorted_results[:10]

        # Return response including similarity scores
        response_data = {'message': 'Query processed', 'query': query, 'results': top_results}
        app.logger.debug("Sending response: %s", response_data)
        return jsonify(response_data)
    elif request.method == 'GET':
        # Handle GET method as before
        query = request.args.get('query')
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        vectorizer = TfidfVectorizer(stop_words=None)
        tfidf_matrix = vectorizer.fit_transform(contents)
        query_vec = vectorizer.transform([query])
        cos_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

        results = [(idx, score) for idx, score in enumerate(cos_similarities)]

        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        top_results = sorted_results[:10]

        return jsonify(top_results)
    else:
        return jsonify({'error': 'Method Not Allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True, port=8000)