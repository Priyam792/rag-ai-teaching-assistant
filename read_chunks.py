import requests

def create_embedding(text):
    r = requests.post("http://localhost:11434/api/embeddings",json={
        "model": "bge-m3",
        "prompt": text
    })

    embedding = r.json()['embedding']
    return embedding

a = create_embedding("cat is good")
print(a)