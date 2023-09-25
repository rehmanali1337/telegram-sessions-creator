from consolemenu.prompt_utils import PromptUtils
from consolemenu.screen import Screen
from telethon import TelegramClient  # pyright: ignore [reportMissingTypeStubs]
from pyrogram.client import Client
import asyncio
from app import gvs
from app.config_reader import config
from app import Console


async def create_telethon_session(phone: str) -> None:
    session_file = f"{gvs.TELETHON_SESSIONS_DIR}/{phone}"
    client = TelegramClient(session_file, api_id=int(config.TELEGRAM_API_ID), api_hash=config.TELEGRAM_API_HASH)
    await client.start(phone=phone)  # pyright: ignore [reportGeneralTypeIssues]
    await client.disconnect()  # pyright: ignore [reportGeneralTypeIssues]
    Console.info(f"Telethon session created at: {session_file}")


async def create_pyrogram_session(phone: str) -> None:
    session_file = f"{gvs.PYROGRAM_SESSIONS_DIR}/{phone}"
    client = Client(
        session_file,
        api_id=int(config.TELEGRAM_API_ID),
        api_hash=config.TELEGRAM_API_HASH,
        phone_number=phone,
    )

    await client.start()
    if client.me and client.me.username:
        Console.info(f"[{client.me.username or client.me.first_name}] login success!")

    try:
        await client.terminate()

    except ConnectionError:
        pass

    try:
        await client.disconnect()

    except ConnectionError:
        pass

    Console.info(f"Pyrogram session created at: {session_file}")


async def main() -> None:
    prompt = PromptUtils(Screen())
    session_types: list[str] = ["Telethon", "Pyrogram"]
    session_type = prompt.prompt_for_numbered_choice(session_types, "Select the type of sessions to create: ")
    while True:
        phone = prompt.input("Enter phone number: ")[0]
        try:
            if session_type == 0:
                await create_telethon_session(phone)
            elif session_type == 1:
                await create_pyrogram_session(phone)
        except Exception as e:
            Console.error(f"Failed to create session. {e}", exc_info=True)
        if prompt.prompt_for_yes_or_no("Do you want to create another session?"):
            continue

        break


if __name__ == "__main__":
    asyncio.run(main())
