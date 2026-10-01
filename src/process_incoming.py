import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity 
import requests


def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed",json={
        "model": "bge-m3",
        "input": text_list
    })

    embedding = r.json()['embeddings']
    return embedding

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate",json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    response = r.json()
    return response

df = joblib.load("embeddings.joblib")


incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0]

similarities = cosine_similarity(np.vstack(df['embedding']) , [question_embedding]).flatten()

top_results = 5
max_indx = similarities.argsort()[::-1][0:top_results]

new_df = df.loc[max_indx]

prompt = f'''You are an AI Teaching Assistant for the Sigma Web Development course.

Your job is to answer the user's questions using ONLY the provided video transcript chunks.

Each chunk contains:
- title: video title
- number: video number
- start: starting timestamp in seconds
- end: ending timestamp in seconds
- text: transcript content

COURSE CONTENT:
{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}

USER QUESTION:
{incoming_query}

INSTRUCTIONS:

1. Understand the user's question and identify the relevant information from the provided course content.

2. Answer naturally and conversationally. Do not mention transcript chunks, JSON, datasets, embeddings, retrieval, or the internal format of the information.

3. If the question is related to the course, tell the user:
   - Which video covers the topic.
   - The video number.
   - The relevant timestamp.
   - What is taught at that point.
   - If multiple videos are relevant, mention all relevant videos in a clear order.

4. Convert timestamps from seconds into a human-readable format:
   - Under 60 seconds → seconds
   - Under 1 hour → minutes:seconds
   - 1 hour or more → hours:minutes:seconds

5. When possible, tell the user where to go in the video, for example:
   "Go to around 12:35 in Video 24, 'JavaScript Functions'."

6. Do not invent information. If the provided course content does not contain enough information to answer the question, clearly say that the available course material does not provide enough information.

7. If the user's question is unrelated to the Sigma Web Development course, respond:
   "I can only answer questions related to the Sigma Web Development course."

8. Keep answers concise but useful. Do not unnecessarily repeat the same information.

9. If the user asks "where is X taught?" or a similar question, prioritize the video title, video number, and timestamp.

10. If the user asks a conceptual question, briefly explain the concept using the retrieved course content and then provide the relevant video and timestamp.

11. Never claim that something is taught in a video unless the provided course content supports it.
'''

response = inference(prompt)['response']
print(response)
