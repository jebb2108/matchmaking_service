import sys

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from services.matching import MatchingService # noqa
from services.notification import NotificationService # noqa
from app.core.config import settings # noqa
from app.core.celeryconfig import app # noqa


matching_service = MatchingService()
notification_service = NotificationService()

@app.task(bind=True, name='process_queue')
async def process_queue():
    """Асинхронная обработка очереди"""
    room_id, user1_id, user2_id = await matching_service.find_match()

    if room_id:
        # Уведомляем пользователей
        await notification_service.notify_match(user1_id, user2_id, room_id)

        # Сохраняем в базу данных
        from db.session import AsyncSessionLocal # noqa
        from models.models import ChatSession # noqa

        async with AsyncSessionLocal() as session:
            chat_session = ChatSession(
                user1_id=user1_id,
                user2_id=user2_id,
                room_id=room_id
            )
            session.add(chat_session)
            await session.commit()

        return f"Match created: {room_id}"

    return "No matches found"