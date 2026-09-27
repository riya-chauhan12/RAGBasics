import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq


#load varibales
load_dotenv()
QDRANT_URL=os.getenv("QDRANT_URL")
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")


#connect to qdrant
client=QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)
print("connected to Qdarant client")

#Create  qdrant collection
COLLECTION_NAME="knowledge"
EMBEDDING_SIZE=384

# delte collection if already exists
if client.collection_exists(COLLECTION_NAME):
    print(f"Deleting existing collection:{COLLECTION_NAME}")
    client.delete_collection(COLLECTION_NAME)


# create collection
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=EMBEDDING_SIZE,
        distance=Distance.COSINE
    ),
)
print(f"Created collection:{COLLECTION_NAME}")
print(f"Vector size:{EMBEDDING_SIZE}")
print("Distance :Cosine")


#load our knowledge
with open("knowledge.txt","r",encoding="utf-8") as f:
    documents=[
        line.strip()
        for line in f
        if line.strip()
    ]
    #["line1","line2"....]
print(f"Loaded {len(documents)} documents")


#create embeddigns
print("loading embedding model....")
model=SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model ready!")

embeddings=model.encode(documents)
print(f"Generated {len(embeddings)} embeddings")
print(f"Embeddigns size: {len(embeddings[0])} ")


#qdrant point

points=[]
for i,embedding in enumerate(embeddings):
    point=PointStruct(
        id=i+1,
        vector=embedding.tolist(),
        payload={
            "text":documents[i]
        }
    )
    points.append(point)

#upload to qdrant
client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)
print(f"uploaded {len(points)} document to qdrant")

#search qdrant
def search(query, top_k=3):
    #conver the question to embedding
    query_vector=model.encode(query).tolist()
    #search in qdrant
    results=client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    ).points
    return results

#test search
query="how many vacation days i can get?"
results=search(query,top_k=3)
print("\n Search Results:")
for result in results:
    print(f"Score:{result.score:.3f}")
    print(result.payload["text"])
    print()


#Connect to GROQ
groq_client=Groq( api_key=GROQ_API_KEY)

 # ASK THE LLM

def ask_llm(question,context):
     prompt=f"""
     Answer the question using the information provided below.
     context:{context} 
     question:{question}
     If the answer is not present in the context,say:
     "I don't know based on the provided informatio."
     """
     response=groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
     )
     return response.choices[0].message.content

# Complete Rag pipleline
question="how many vactions do I get?"
results=search(question,top_k=3)

#extract from the search result
context="\n".join(
    result.payload["text"]
    for result in results
 )
answer =ask_llm(question,context)
print("\n final answer")
print(answer)
