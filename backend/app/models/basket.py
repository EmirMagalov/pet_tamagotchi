from tortoise import fields, models

class Basket(models.Model):
    id = fields.IntField(pk=True)
    pet = fields.ForeignKeyField('models.Pet', related_name='items')
    item_id = fields.IntField()  # Просто ID из твоего JS/Python списка
    quantity = fields.IntField(default=1)

    class Meta:
        table = "Basket"
