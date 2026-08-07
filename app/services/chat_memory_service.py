import redis

from app.core.config import REDIS_HOST, REDIS_PORT


class ChatMemoryService:
    def __init__(self):
        self.redis = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
        )

    def get_history(self, session_id: str):
        history = self.redis.lrange(session_id, 0, -1)
        return history

    def add_message(self, session_id: str, role: str, content: str):
        self.redis.rpush(session_id, f"{role}: {content}")

        # Keep only the last 20 messages
        self.redis.ltrim(session_id, -20, -1)


chat_memory_service = ChatMemoryService()