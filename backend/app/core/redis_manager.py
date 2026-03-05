import json
import asyncio
import redis.asyncio as aioredis
from websocket.ws_manager import ConnectionManager


manager = ConnectionManager()

REDIS_URL = "redis://localhost:6379"


async def redis_listener():
    redis = aioredis.from_url(f"{REDIS_URL}/0", decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe("game_updates")
    print("✅ Redis listener: подписались на game_updates")

    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            try:
                data = json.loads(message["data"])
            except json.JSONDecodeError:
                print("❌ Не JSON пришёл:", message["data"])
                continue

            target_id = data.get("tg_id")
            if not target_id:
                print("⚠️ В сообщении нет tg_id")
                continue

            print(f"→ Получено обновление для tg_id={target_id}")
            if target_id in manager.active_connections:
                await manager.send_personal_message(data, target_id)
            else:
                print(f"   Игрок {target_id} не в active_connections")
    except Exception as e:
        print(f"❌ Критическая ошибка listener: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await pubsub.close()
