from tortoise.models import Model
from tortoise import fields


class User(Model):
    user_id = fields.IntField()
    guild_id = fields.IntField()
    level = fields.IntField(default=1)
    exp = fields.IntField(default=0)
    coins = fields.IntField(default=0)
    active = fields.BooleanField(default=True)
    blocked = fields.BooleanField(default=False)

    class Meta:
        table = "users"
        unique_together = (("user_id", "guild_id"),)

    @property
    def level_up_exp(self) -> int:
        return int(83 + 83 * 2 * (self.level - 1))
