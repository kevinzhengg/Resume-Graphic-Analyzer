import chromadb
client = chromadb.PersistentClient(path="~/.chromadb")
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection")