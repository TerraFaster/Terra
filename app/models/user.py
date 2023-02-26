import math
from tortoise.models import Model
from tortoise import fields


BASE_LEVEL_EXP = 83


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
        return self.__level_up_exp(self.level)
    
    @staticmethod
    def __level_up_exp(current_level: int) -> int:
        """Calculates experience points needed to level up.

        Args:
            `current_level` (`int`): Current level.

        Returns:
            `int`: Experience points needed to level up.
        """
        return int((current_level - 1) * 83 + math.sqrt(current_level * 10) * 83)

    async def add_exp(self, exp: int) -> None | int:
        """Adds experience points to user.

        Args:
            `exp` (`int`): Experience points.

        Returns:
            `int` | `None`: New level if leveled up, otherwise `None`.
        """
        self.exp += exp
        new_level = None

        if self.exp >= self.level_up_exp:
            new_level = 1

            while self.exp >= self.__level_up_exp(new_level):
                new_level += 1

            self.coins += new_level - self.level
            self.level = new_level
            self.exp -= self.__level_up_exp(new_level - 1)

        await self.save()
        return new_level
