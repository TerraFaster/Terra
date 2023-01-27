from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "guilds" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "prefix" VARCHAR(5) NOT NULL  DEFAULT '!'
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INT NOT NULL,
    "guild_id" INT NOT NULL,
    "level" INT NOT NULL  DEFAULT 1,
    "exp" INT NOT NULL  DEFAULT 0,
    "coins" INT NOT NULL  DEFAULT 0,
    "active" INT NOT NULL  DEFAULT 1,
    "blocked" INT NOT NULL  DEFAULT 0,
    CONSTRAINT "uid_users_user_id_c96ac4" UNIQUE ("user_id", "guild_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
