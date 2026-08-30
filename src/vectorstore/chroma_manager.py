import chromadb

client = chromadb.PersistentClient(
    path= "data/vectordb"
    )

collection = client.get_or_create_collection(
    "enterprise_documents"
    )

#tp knoe how many uplloads done
# print(

#     collection.count()

# )

# results = collection.get()

# print(results)



