import asyncpg

from app.services.matching import MatchingService # noqa
from app.services.notification import NotificationService # noqa
from app.core.config import settings # noqa
from app.core.celeryconfig import app # noqa

from app.db.database import Database

db = None
matching_service = MatchingService()
notification_service = NotificationService()

@app.task(bind=True, name='process_queue')
async def process_queue():
    """Асинхронная обработка очереди"""
    global db
    if db is None: db = Database(asyncpg.connect(dsn=settings.POSTGRES_URL))

    room_id, user1_id, user2_id = await matching_service.find_match()

    if room_id:
        # Уведомляем пользователей
        await notification_service.notify_match(user1_id, user2_id, room_id)
        await db.add_chat_session(user1_id, user2_id, room_id)
        return f"Match created: {room_id}"

    return "No matches found"