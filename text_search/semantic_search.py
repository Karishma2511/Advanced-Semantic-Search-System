import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open('/Users/karishmamajeeth/PycharmProjects/Advanced-Semantic-Search-System /mycrawler/mycrawler/arxiv_papers.json') as f:
    documents = json.load(f)
contents = [doc['abstract'] for doc in documents if 'abstract' in doc]

vectorizer = TfidfVectorizer(stop_words=None)
tfidf_matrix = vectorizer.fit_transform(contents)

def search(query):
    query_vec = vectorizer.transform([query])
    cos_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    return cos_similarities

query = "machine learning applications"
similarities = search(query)
print(similarities)

# Get the titles for each document, assuming each has a 'title' field
titles = [doc['title'] for doc in documents if 'abstract' in doc]

# Combine titles and similarities into a list of tuples
titled_similarities = list(zip(titles, similarities))

# Sort the list of tuples by similarity score, highest first
sorted_similarities = sorted(titled_similarities, key=lambda x: x[1], reverse=True)

# Display the top N results
top_n = 3
for title, score in sorted_similarities[:top_n]:
    print(f"Title: {title}, Similarity: {score}")