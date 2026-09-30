import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity 
import requests

df = joblib.load("embeddings.joblib")

def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed",json={
        "model": "bge-m3",
        "input": text_list
    })

    embedding = r.json()['embeddings']
    return embedding

income_query = input("Ask a Question: ")
question_embedding = create_embedding([income_query])[0]

similarities = cosine_similarity(np.vstack(df['embedding']) , [question_embedding]).flatten()
# print(similarities)

top_results = 8
max_indx = similarities.argsort()[::-1][0:top_results]
# print(max_indx)

new_df = df.loc[max_indx]
# print(new_df[['number','title','text']])

prompt = f'''
I am teaching web development cource usign Sigma web development course. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df.to_json}
-------------------------------------
"{income_query}"
User asked this question related to the video chunks , you have to answer where and how much content is taught (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, tell him that you can only answer questions related to the course.
'''


for index , item in new_df.iterrows():
    print(index,item['title'],item['number'],item['text'],item['start'],item['end'])