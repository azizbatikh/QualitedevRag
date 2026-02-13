import os
import weaviate
from weaviate.classes.query import Filter

with weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ["WEAVIATE_URL"],
    auth_credentials=os.environ["WEAVIATE_API_KEY"],
) as client:

    nutrition = client.collections.use("NutritionChunk")

    response = nutrition.query.hybrid(
        query="alimentation saine",
        alpha=0.7,
        limit=5
    )

    for obj in response.objects:
        print(obj.properties)
