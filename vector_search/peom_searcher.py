from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent


class PeomSearcher:
    """
    古诗词搜索
    """

    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer(
            str(
                BASE_DIR
                / "vector_search"
                / "models"
                / "sentence-transformers-all-MiniLM-L6-v2"
            ),
            device="cpu",
        )
        self.client = QdrantClient(":memory:")
        self.load_json_data(BASE_DIR / "scripts" / "simple_poems.json")

    @staticmethod
    def remove_space_and_newline(text):
        return text.replace(" ", "").replace("\n", ",")

    def load_json_data(self, data_path):
        """
        加载数据
        """
        try:
            with open(data_path, "r") as file:
                documents = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"{data_path} not found. please excute scripts/siloder_poems.py first and execute  scripts/deal_poems.py"
            )
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.model.get_sentence_embedding_dimension(),  # Vector size is defined by used model
                distance=models.Distance.COSINE,  # 使用余弦
            ),
        )
        points = []
        for idx, doc in enumerate(documents):
            points.append(
                models.PointStruct(
                    id=idx,
                    vector=self.model.encode(
                        self.remove_space_and_newline(doc["content"])
                    ).tolist(),
                    payload=doc,
                )
            )
        self.client.upload_points(collection_name=self.collection_name, points=points)
        print(
            f"Loaded {len(documents)} documents into collection {self.collection_name}"
        )

    def search(self, query, limit=1):
        """
        搜索
        """
        query_embedding = self.model.encode(self.remove_space_and_newline(query))
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.tolist(),
            limit=limit,
        )
        return [doc.payload for doc in results]
