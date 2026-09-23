import os
from pathlib import Path
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer

def cosine_similarity(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)
    )

model=SentenceTransformer("all-MiniLM-l6-v2") #384
text="Machine Learning is fun"

#embedding=model.encode(text)
#print(embedding.shape)
#printing starting 10
#print(embedding[:10])

#t1="there are 20 paid leaves"
t1="the pizza is good"
t2="there are 24 vacations days"
v1=model.encode(t1)
v2=model.encode(t2)

print(cosine_similarity(v1,v2))