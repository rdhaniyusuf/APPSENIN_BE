import bcrypt
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, create_engine
import asyncio


# Inisialisasi Database (SQLite untuk testing)
DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/appsenindb"
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Model User
class User(Base):
    __tablename__ = "at_sys_msuser"
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    user_pass = Column(String)
    is_active = Column(Boolean, default=True)


# Fungsi untuk Hash Password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# Fungsi untuk Cek Password
def check_password(password: str, hashed_password: str) -> bool:
    bcrypt.gensalt(rounds=15, prefix=b'2b')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


# Simpan User ke Database Secara Asinkron
async def create_user():
    async with SessionLocal() as session:
        async with session.begin():
            user = User(user_name="appsenin.admin", user_pass=hash_password("secureAdmin#2025"))
            session.add(user)
            await session.commit()


# Login User Asinkron
async def login_user(user_name: str, password: str):
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter(User.user_name == user_name))
        user = result.scalars().first()
        
        if not user:
            print("User not found")
            return False
        
        if not user.user_pass:
            print("No password stored in database!")
            return False
        
        if not check_password(password, user.user_pass):
            print("Incorrect password")
            return False
        
        print("Login successful!")
        return True


# Menjalankan Tes
async def test():
    # await create_user()
    await login_user("appsenin.admin", "secureAdmin#2025")
# await test()

# Menjalankan Tes Secara Synchronous
asyncio.run(test())