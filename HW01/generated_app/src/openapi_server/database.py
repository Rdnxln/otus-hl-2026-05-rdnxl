import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

CONNECT_INFO = os.getenv( "CONNECT_INFO", "postgresql+asyncpg://app_user:321!123@localhost:5432/sn" )

engine = create_async_engine( CONNECT_INFO, echo=True )
AsyncSessionLocal = async_sessionmaker( bind=engine, expire_on_commit=False )
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
