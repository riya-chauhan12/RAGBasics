import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams,PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq

#load varibales
load_dotenv()
QDRANT_URL=od.getenv("QDRANT_URL")
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

#delte collection if already exists
if client.collection_exits(COLLECTION_NAME):
    print(f"Deleting existing collection:{COLLECTION_NAME}")
    client.delete_collection(COLLECTION_NAME)
#create collectin
client.create.collection(
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
        for line in f:
        if line.strin()
    ]
    #["line1","line2"....]
print(f"Loaded {len(documents)} documents")

#create embeddigns
print("loading embedding model....")
model=SenteceTransformer("all-MiniLM-L6-v2")

print("Embedding model ready!")

embeddings=model.encode(documents)
print(f"Generated {len(embeddings)} embeddings")
print(f"Embeddigns size: {len(embeddings[0])} ")


#qdrant point

points=[]
for i,embeddings in enumerate(embeddings):
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
quey="how many vaction days i can get?"
results=serach(query,top_k=3)
print("\n Search Results:")
for result in results:
    print(f"Score:{result.score:.3f}")
    print(result.payload["text"])
    print()


