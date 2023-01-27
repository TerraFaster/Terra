from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "guilds" ADD "newcomer_roles" JSON NOT NULL DEFAULT [];"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "guilds" DROP COLUMN "newcomer_roles";"""
