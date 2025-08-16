from langchain.vectorstores import PGVector
from langchain.embeddings import OpenAIEmbeddings
from decouple import config
from typing import Dict


class VectorStoreSingleton:
    _instances: Dict[str, PGVector] = {}

    @classmethod
    def get_instance(cls, collection_name: str = "paints_collection") -> PGVector:
        if collection_name not in cls._instances:
            cls._instances[collection_name] = cls._create_vector_store(collection_name)
        return cls._instances[collection_name]

    @classmethod
    def _create_vector_store(cls, collection_name: str) -> PGVector:
        return PGVector(
            embedding_function=OpenAIEmbeddings(
                api_key=config("OPENAI_API_KEY"), 
                model="text-embedding-3-large"
            ),
            connection_string=config('DATABASE_URL'),
            collection_name=collection_name,
            use_jsonb=True
        )
