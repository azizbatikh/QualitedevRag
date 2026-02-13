import weaviate
from weaviate.classes.config import Configure, Property, DataType

COLLECTION = "NutritionChunk"

WEAVIATE_URL = "isgeqevrhogbtnym8k2hg.c0.europe-west3.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "cm5lT2YyZ0lUcnByczlBTl9idzZPenJUZ2Nmamg2dXJBUk1UbDVMWG5rUmxLTmtSY2s2dytpT3UzdjF3PV92MjAw"

with weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=WEAVIATE_API_KEY,
) as client:

    # dev only: repartir propre
    if client.collections.exists(COLLECTION):
        client.collections.delete(COLLECTION)
        print(f"🗑️ Deleted existing collection: {COLLECTION}")

    client.collections.create(
        name=COLLECTION,
        # Vectorisation automatique (embeddings gérés côté Weaviate Cloud)
        vector_config=Configure.Vectors.text2vec_weaviate(),
        properties=[
            Property(name="text", data_type=DataType.TEXT),
            Property(name="category", data_type=DataType.TEXT),      # macros / vitamines / regimes / oms
            Property(name="source", data_type=DataType.TEXT),        # "cours", "oms", etc.
            Property(name="title", data_type=DataType.TEXT),         # titre doc
            Property(name="chunk_index", data_type=DataType.INT),    # position dans le doc
            Property(name="tags", data_type=DataType.TEXT_ARRAY),    # ["proteines","energie"]
        ],
    )

    print(f"✅ Created collection: {COLLECTION}")
