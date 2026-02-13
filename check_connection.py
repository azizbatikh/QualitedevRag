import os
import weaviate

weaviate_url = "isgeqevrhogbtnym8k2hg.c0.europe-west3.gcp.weaviate.cloud"
weaviate_api_key = "cm5lT2YyZ0lUcnByczlBTl9idzZPenJUZ2Nmamg2dXJBUk1UbDVMWG5rUmxLTmtSY2s2dytpT3UzdjF3PV92MjAw"

with weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=weaviate_api_key,
) as client:
    print("Connected:", client.is_ready())
