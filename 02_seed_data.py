import weaviate

COLLECTION = "NutritionChunk"

WEAVIATE_URL = "isgeqevrhogbtnym8k2hg.c0.europe-west3.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "cm5lT2YyZ0lUcnByczlBTl9idzZPenJUZ2Nmamg2dXJBUk1UbDVMWG5rUmxLTmtSY2s2dytpT3UzdjF3PV92MjAw"

seed = [
    {"text": "Les protéines participent à la construction et réparation des tissus. Elles sont importantes pour les muscles.",
     "category": "macros", "source": "cours", "title": "Bases nutrition", "chunk_index": 0, "tags": ["proteines", "muscles"]},

    {"text": "Les glucides sont une source d’énergie majeure, notamment pour le cerveau. On privilégie les glucides complexes.",
     "category": "macros", "source": "cours", "title": "Bases nutrition", "chunk_index": 1, "tags": ["glucides", "energie"]},

    {"text": "Les lipides sont importants pour les membranes cellulaires et certaines hormones. Sources: huile d’olive, noix, poissons gras.",
     "category": "macros", "source": "cours", "title": "Bases nutrition", "chunk_index": 2, "tags": ["lipides", "omega3"]},

    {"text": "La vitamine C contribue au système immunitaire. On la trouve dans les agrumes, kiwi, poivrons.",
     "category": "vitamines", "source": "cours", "title": "Vitamines", "chunk_index": 0, "tags": ["vitamine C", "immunite"]},

    {"text": "La vitamine D contribue au maintien d’une ossature normale. Soleil + poissons gras.",
     "category": "vitamines", "source": "cours", "title": "Vitamines", "chunk_index": 1, "tags": ["vitamine D", "os"]},

    {"text": "Le régime méditerranéen favorise légumes, fruits, huile d’olive, légumineuses, poisson. Bon équilibre global.",
     "category": "regimes", "source": "cours", "title": "Régimes", "chunk_index": 0, "tags": ["mediterraneen", "equilibre"]},

    {"text": "OMS: limiter les aliments ultra-transformés riches en sel, sucres et graisses saturées.",
     "category": "oms", "source": "oms", "title": "Recommandations OMS", "chunk_index": 0, "tags": ["oms", "ultra-transformes"]},

    {"text": "OMS: augmenter fruits et légumes pour les fibres, vitamines et minéraux.",
     "category": "oms", "source": "oms", "title": "Recommandations OMS", "chunk_index": 1, "tags": ["oms", "fruits", "legumes"]},
]

with weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=WEAVIATE_API_KEY,
) as client:
    col = client.collections.use(COLLECTION)

    with col.batch.fixed_size(batch_size=50) as batch:
        for obj in seed:
            batch.add_object(properties=obj)

    print(f"✅ Inserted {len(seed)} objects into {COLLECTION}")
