import os
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
model=SentenceTransformer("all-MiniLM-L6-v2")

 
load_dotenv()
my_api=os.getenv("GROQ_API")
if not my_api:
    raise ValueError(" api key not found")

client=Groq(api_key=my_api)
modelgroq="openai/gpt-oss-120b"

#knowledge base
documents=[
    "Employeed recieve 24 days of paid leave per year.",
    "Monday and Friday are optional work-from-home days.",
    "Employees recieve Rs 3000 per month for gym reimbursement.",
    "Employees can claim Rs 2000 per month from home internet.",
    "Emplyees have a 90 day notice period."
]

document_embed=model.encode(documents)
def cosine_similarity(a,b):
    return np.dot(a,b)/(
    np.linalg.norm(a) *np.linalg.norm(b)
    )

def retrive(query_emb):
    scores=[]
    for i,document in enumerate(document_embed):
        score=cosine_similarity(query_emb,document)
        scores.append((score,documents[i]))

    scores.sort(reverse=True)
    return scores[0] #will return the highest score

def ask_llm(question,context):
    sys_prompt=f""" answer in one line only. Answer only based on this context. do not hallucinate.Context:{context}"""
    system_message={
        "role":"system",
        "content":sys_prompt
    }
    message={
        "role":"user",
        "content":question
    }
    messages=[system_message,message]
    response=client.chat.completions.create(model=modelgroq,messages=messages)
    answer=response.choices[0].message.content
    return answer



query="How much leave I can get ?"

#without using gork llm

query_emb=model.encode(query)
score,context=retrive(query_emb)
#print(score)
#print(context) 
answer=ask_llm(query,context)
print(answer)






