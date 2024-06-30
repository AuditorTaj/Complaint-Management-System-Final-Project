from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres:5432/complaints"

# Asynchronous engine for application use
async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# Synchronous engine for Alembic migrations
sync_engine = create_engine(DATABASE_URL.replace('asyncpg', 'psycopg2'), echo=True)
sync_session = sessionmaker(bind=sync_engine)

async def get_db():
    async with async_session() as session:
        yield session

Base = declarative_base()
