import sys

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from services.matching import MatchingService # noqa


router = APIRouter()

@router.post("/search/{user_id}")
async def start_search(
    user_id: int,
    matching_service: MatchingService = Depends()
):
    """Начать поиск собеседника"""
    user_data = {
        "tg_id": user_id,
        "joined_at": datetime.now().isoformat()
    }
    await matching_service.add_to_queue(user_id, user_data)
    return {"status": "searching"}

@router.delete("/search/{user_id}")
async def cancel_search(
    user_id: int,
    matching_service: MatchingService = Depends()
):
    """Отменить поиск собеседника"""
    await matching_service.remove_from_queue(user_id)
    return {"status": "cancelled"}

@router.get("/status/{user_id}")
async def search_status(
    user_id: int,
    matching_service: MatchingService = Depends()
):
    """Проверить статус поиска"""
    is_searching = await matching_service.redis.exists(f"searching:{user_id}")
    return {"searching": bool(is_searching)}