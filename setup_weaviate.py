import os
import weaviate

from weaviate.classes.config import Configure, Property, DataType


with weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ["WEAVIATE_URL"],
    auth_credentials=os.environ["WEAVIATE_API_KEY"],
) as client:

    # Création de la collection
    client.collections.create(
        name="NutritionChunk",
        vector_config=Configure.Vectors.text2vec_weaviate(),
        properties=[
            Property(name="text", data_type=DataType.TEXT),
            Property(name="source", data_type=DataType.TEXT),
            Property(name="category", data_type=DataType.TEXT),
        ],
    )



    print("Collection NutritionChunk créée !")
