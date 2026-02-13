import os
import weaviate

with weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ["WEAVIATE_URL"],
    auth_credentials=os.environ["WEAVIATE_API_KEY"],
) as client:

    nutrition = client.collections.use("NutritionChunk")

    data = [
        {
            "text": "Les protéines aident à développer les muscles.",
            "source": "OMS",
            "category": "protéines"
        },
        {
            "text": "Les glucides donnent de l'énergie au corps.",
            "source": "OMS",
            "category": "glucides"
        },
        {
            "text": "Les lipides sont importants pour le cerveau.",
            "source": "OMS",
            "category": "lipides"
        },
        {
            "text": "Il est recommandé de manger 5 fruits et légumes par jour.",
            "source": "OMS",
            "category": "recommandations"
        }
    ]

    with nutrition.batch.fixed_size(batch_size=10) as batch:
        for obj in data:
            batch.add_object(properties=obj)

print("Données nutrition ajoutées !")
