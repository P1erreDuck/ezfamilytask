import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv
from back.app.db.base import Base
from back.app.models.item import Item

load_dotenv()
url = os.getenv("DATABASE_URL")
db_name = url.split('/')[-1]


async def reset():
    if input("Сбросить БД? (д/н): ").lower() not in ['д', 'да', 'y', 'yes']:
        return

    admin_engine = create_async_engine(
        url.replace(f'/{db_name}', '/postgres'),
        isolation_level="AUTOCOMMIT"
    )

    async with admin_engine.connect() as conn:
        await conn.execute(text(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{db_name}'
        """))
        await conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        await conn.execute(text(f"CREATE DATABASE {db_name}"))

    await admin_engine.dispose()

    main_engine = create_async_engine(url)

    async with main_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await main_engine.dispose()


asyncio.run(reset())