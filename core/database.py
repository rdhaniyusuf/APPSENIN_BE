from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Inisialisasi engine untuk async mode
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Base class untuk model SQLAlchemy
Base = declarative_base()

# Session factory untuk membuat sesi database
SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency untuk mendapatkan session database
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
