from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from datetime import datetime, timezone
from bson import ObjectId
from .config import settings

_client: Optional[AsyncIOMotorClient] = None

def get_database() -> AsyncIOMotorDatabase:
    """
    Retorna a instância do banco de dados MongoDB
    """
    global _client
    if _client is None:
        if not settings.MONGO_URL:
            raise RuntimeError("MONGO_URL não está definido no arquivo .env")
        _client = AsyncIOMotorClient(settings.MONGO_URL)
    return _client[settings.MONGO_DB]

def serialize_message(doc: dict) -> Dict:
    """
    Serializa um documento do MongoDB para um formato JSON
    """
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
        del doc["id"]

    if "created_at" in doc and isinstance(doc["created_at"], datetime):
        if doc["created_at"].tzinfo is None:
            doc["created_at"] = doc["created_at"].replace(tzinfo=timezone.utc)
        doc["created_at"] = doc["created_at"].isoformat().replace("+00:00", "Z")
    
    return doc