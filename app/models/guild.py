from tortoise.models import Model
from tortoise import fields


class Guild(Model):
    id = fields.IntField(pk=True)
    prefix = fields.CharField(max_length=5, default="!")
    
    class Meta:
        table = "guilds"
