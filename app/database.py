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

def serialize_message(doc: dict[str, Any]) -> Dict[str, Any]:
    """
    Serializa um documento do MongoDB para um formato JSON
    """
    serialized = doc.copy()

    if "_id" in serialized:
        print("-> Campo '_id' encontrado. Convertendo para 'id'.")
        serialized["id"] = str(serialized["_id"])
        del serialized["_id"]
    if "created_at" in serialized and isinstance(serialized["created_at"], datetime):
        if serialized["created_at"].tzinfo is None:
            serialized["created_at"] = serialized["created_at"].replace(tzinfo=timezone.utc)
        serialized["created_at"] = serialized["created_at"].isoformat().replace("+00:00", "Z")
    
    return serialized