import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api=os.getenv("GROQ_API")
if not my_api:
    raise ValueError(" api key not found")

Client=Groq(api_key=my_api)
model="openai/gpt-oss-120b"

#step1(make knowlwege base)
knowledge_base={
    "age" : " The age of Alice is 30 years",
    "net worth" : "The net worth of Alice is 20cr"
}
#step 2: retreival
def retrive_info(question):
    question=question.lower()
    if "age" in  question:
        return knowledge_base["age"]
    elif "net worth" in question:
        return knowledge_base["net worth"]
    else:
        return None

    
def ask_llm(question):
    context=retrive_info(question)

    sys_prompt=f""" answer in one line only. Answer based on this context. do not hallucinate. Context:{context}"""
    system_message={
        "role":"system",
        "content":sys_prompt
    }
    message={
        "role":"user",
        "content":question
    }
    response=Client.chat.completions.create(model=model,messages=[system_message,message])
    answer=response.choices[0].message.content
    return answer

question="what is alice age"
print(ask_llm(question))