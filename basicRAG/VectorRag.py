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
