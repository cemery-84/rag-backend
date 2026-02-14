from azure.cosmos import CosmosClient, PartitionKey
import os

COSMOS_URI = os.getenv("COSMOS_URI")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE = os.getenv("COSMOS_DATABASE")

COSMOS_USERS_CONTAINER = os.getenv("COSMOS_USERS_CONTAINER")
COSMOS_CONVERSATIONS_CONTAINER = os.getenv("COSMOS_CONVERSATIONS_CONTAINER")
COSMOS_MESSAGES_CONTAINER = os.getenv("COSMOS_MESSAGES_CONTAINER")

client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
database = client.get_database_client(COSMOS_DATABASE)

users_container = database.get_container_client(COSMOS_USERS_CONTAINER)
conversations_container = database.get_container_client(COSMOS_CONVERSATIONS_CONTAINER)
messages_container = database.get_container_client(COSMOS_MESSAGES_CONTAINER)