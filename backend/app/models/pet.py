from tortoise import fields, models
from datetime import datetime, timezone


class Pet(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    name = fields.CharField(max_length=50, null=True, blank=True)
    money = fields.FloatField(default=100.0)

    # Это "снимки" (snapshots) состояния на момент последнего обновления
    hunger = fields.FloatField(default=100.0)
    energy = fields.FloatField(default=100.0)
    dirt = fields.FloatField(default=0.0)
    # Убираем auto_now=True, будем обновлять вручную при действиях
    last_updated = fields.DatetimeField(auto_now_add=True)

    is_sleeping = fields.BooleanField(default=False)
    wake_up_at = fields.BigIntField(default=0)

    class Meta:
        table = "pets"




