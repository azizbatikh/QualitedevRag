import weaviate
from weaviate.classes.query import Filter

COLLECTION = "NutritionChunk"

WEAVIATE_URL = "isgeqevrhogbtnym8k2hg.c0.europe-west3.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "cm5lT2YyZ0lUcnByczlBTl9idzZPenJUZ2Nmamg2dXJBUk1UbDVMWG5rUmxLTmtSY2s2dytpT3UzdjF3PV92MjAw"

with weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=WEAVIATE_API_KEY,
) as client:
    col = client.collections.use(COLLECTION)

    res = col.query.near_text(
        query="vitamine pour les os",
        limit=3,
        filters=Filter.by_property("category").equal("vitamines")
    )

    print("=== category=vitamines ===")
    for obj in res.objects:
        print("-", obj.properties["text"])
