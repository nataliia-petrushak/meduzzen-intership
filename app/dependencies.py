from sqlalchemy.ext.asyncio import AsyncSession

from db.database import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
