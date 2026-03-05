import os



from taskiq import TaskiqScheduler
from taskiq_redis import ListQueueBroker
from taskiq.schedule_sources import LabelScheduleSource
from tortoise import Tortoise
from core.publish_redis import publish
from models.pet import Pet as PetModel
# 1. Настройка брокера
broker = ListQueueBroker("redis://localhost:6379/0")

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


# Функция для жесткой инициализации базы
async def ensure_db_connected():
    if not Tortoise._inited:
        # Пытаемся найти файл базы. Если ты в папке app, он лежит там.
        # Если нет — ищем на уровень выше.
        db_path = os.path.join(os.getcwd(), "db.sqlite3")

        await Tortoise.init(
            db_url=f"sqlite://{db_path}",
            modules={"models": ["models.pet"]}
        )
        print(f"✅ База подключена по пути: {db_path}")


@broker.task(schedule=[{"cron": "* * * * *"}])
async def heavy_task():


    # ПРИНУДИТЕЛЬНО ПОДКЛЮЧАЕМСЯ
    await ensure_db_connected()
    all_pets = await PetModel.all()
    if not all_pets:
        return

    for pet in all_pets:
       await publish(pet)



# python -m taskiq worker tasks.tkq:broker

# python -m taskiq scheduler tasks.tkq:scheduler