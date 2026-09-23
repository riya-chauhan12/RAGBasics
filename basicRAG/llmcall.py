#os allow python to interact with thw operating system
import os
#dotenv allow python to read variable stored in .env file
from dotenv import load_dotenv
#import groq python client 
#it allows python program to communicate with groq Api
from groq import Groq
load_dotenv()
# used os to read api key form .env file
my_api=os.getenv("GROQ_API")
if not my_api:
    raise ValueError("APi key is inavailabe")

#create gorq client object
client=Groq(api_key=my_api)
model="openai/gpt-oss-120b"

role="user"
prompt="tell me about google"

#This is the format expected by the chat API.
message={
    "role":role,
    "content":prompt
}
messages=[message]

response=client.chat.completions.create(model=model,messages=messages)
# this print object returned by groq
#It will contain more than just the answer—things 
#like model information, usage/token information, etc.
print(response)
'''
print(response.choices[0].message.content)
response
 └── choices
      └── [0]
           └── message
                └── content
                     └── "Yes, I know about Google..."

'''


