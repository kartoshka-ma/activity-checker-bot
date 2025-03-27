from aiogram import Dispatcher, types, Bot
from aiogram.utils import executor
from dotenv import load_dotenv
from database import Database
from os import getenv
import asyncio
import asyncpg

load_dotenv()
bot = Bot(token=getenv("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start_command(message: types.Message) -> None:
    await message.reply("\n/satrt - помощь по командам\n"
                        "/top - список топа по сообщениям в группе")

@dp.message_handler(commands="top")
async def top_commad(message: types.Message) -> None:
    chat_id = message.chat.id
    async with Database(getenv("DATABASE_URL")) as db:
        query = """
                SELECT *
                FROM groups 
                WHERE chat_id = $1
                ORDER BY messages_count DESC
                LIMIT 5;
                """
        top_users = await db.connection.fetch(query, chat_id)
    
    if not top_users:
        await message.answer("Пока никто не написал сообщений 😔")
        return
    
    leaderboard = "🏆 *Топ-5 активных участников чата:*\n\n"
    for i in range(len(list(top_users))):
        count = top_users[i]["messages_count"]
        first_name = top_users[i]["first_name"]
        last_name = top_users[i]["last_name"]
        user_id = top_users[i]["user_id"]
        mention = f"[{first_name or ''} {last_name or ''}](tg://user?id={user_id})"
        leaderboard += f"{i+1}. {mention} — *{count} сообщений* 📩\n"

    await message.reply(leaderboard, parse_mode="Markdown")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def new_message(message: types.Message) -> None:
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    async with Database(getenv("DATABASE_URL")) as db:
        await db.insert_data((chat_id, user_id, username, first_name, last_name))

async def main() -> None:
    print("Bot is running...")
    async with Database(getenv("DATABASE_URL")) as db:
        await db.create_table()    
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
