from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, HTTPException, status
from bson import ObjectId
from datetime import datetime, timezone
from ..database import get_database, serialize_message
from ..models import MessageIn, MessageOut
from ..ws_manager import manager

router = APIRouter()
DB_COLLECTION = "messages"

@router.get("/rooms/{room}/messages", response_model=dict)
async def get_messages(
    room: str,
    limit: int = Query(20, ge=1, le=100),
    before_id: str | None = Query(None),
):
    db = get_database()
    query = {"room": room}

    if before_id:
        try:
            query["_id"] = {"$lt": ObjectId(before_id)}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O valor de before_id '{before_id}' não é um Id válido.",
            )
    cursor = db[DB_COLLECTION].find(query).sort("_id", -1).limit(limit)
    docs = [serialize_message(d) async for d in cursor]
    docs.reverse()

    next_cursor = docs[0]["_id"] if docs else None
    return {"items": [MessageOut(d) for d in docs], "next_cursor": next_cursor}

@router.post("/rooms/{room}/messages", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def post_message(room: str, message_in: MessageIn):
    db = get_database()

    doc = {
        "room": room,
        "username": message_in.username,
        "content": message_in.content,
        "created_at": datetime.now(timezone.utc),
    }              
    res = await db[DB_COLLECTION].insert_one(doc)
    doc["_id"] = res.inserted_id

    serialized_doc = serialize_message(doc)
    return MessageOut(serialized_doc)

@router.websocket("/ws/{room}")
async def ws_room(ws: WebSocket, room: str):
    await manager.connect(room, ws)
    db = get_database()
    try:
        cursor = db[DB_COLLECTION].find({"room": room}).sort("_id", -1).limit(20)
        items = [serialize_message(d) async for d in cursor]
        items.reverse()
        await ws.send_json({
            "type": "history",
            "items": [MessageOut(i) for i in items]
        })

        while True:
            payload = await ws.receive_json()
            message = MessageIn(**payload)
            doc = {
                "room": room,
                "username": message.username,
                "content": message.content,
                "created_at": datetime.now(timezone.utc),
            }
            res = await db[DB_COLLECTION].insert_one(doc)
            doc["_id"] = res.inserted_id

            serialized_doc = serialize_message(doc)
            await manager.broadcast(room, {"type": "message", "item": MessageOut(serialized_doc).model_dump()})
    except WebSocketDisconnect:
        manager.disconnect(room, ws)

