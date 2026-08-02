import json
import pickle

from sklearn.metrics.pairwise import cosine_similarity

vectorizer = pickle.load(open("processed/retrieval/tfidf.pkl","rb"))
matrix = pickle.load(open("processed/retrieval/matrix.pkl","rb"))
metadata = json.load(open("processed/retrieval/metadata.json"))

print("="*70)
print("GOHIF Retrieval Engine")
print("Type 'exit' to quit")
print("="*70)

while True:

    query = input("\nGOHIF> ")

    if query.lower() == "exit":
        break

    q = vectorizer.transform([query])

    scores = cosine_similarity(q,matrix)[0]

    order = scores.argsort()[::-1][:10]

    print()

    for i in order:

        if scores[i] <= 0:
            continue

        print(f"{metadata[i]}   score={scores[i]:.3f}")
