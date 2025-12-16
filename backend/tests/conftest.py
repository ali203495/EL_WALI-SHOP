import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

# Use an in-memory SQLite database for tests to ensure isolation
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """Create an async client with the overridden database dependency."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def admin_token(db_session, client):
    """Create a super admin user and return a valid access token."""
    from models import User
    from auth import get_password_hash
    
    # Check if user exists (in case logic runs on shared DB, though we use isolated DB for now)
    # Using the session given by db_session
    
    admin_user = User(
        username="pytest_admin",
        hashed_password=get_password_hash("admin123"),
        email="admin@test.com",
        first_name="Test",
        last_name="Admin",
        phone_number="000111",
        is_admin=True,
        is_super_admin=True,
        is_active=True
    )
    db_session.add(admin_user)
    await db_session.commit()
    
    response = await client.post("/token", data={"username": "pytest_admin", "password": "admin123"})
    return response.json()["access_token"]

@pytest_asyncio.fixture
async def super_admin_token(db_session, client):
    from models import User
    from auth import get_password_hash
    
    # Create Super Admin
    admin_user = User(
        username="superadmin",
        hashed_password=get_password_hash("admin123"),
        email="super@test.com",
        first_name="Super",
        last_name="Admin",
        phone_number="000",
        is_admin=True,
        is_super_admin=True,
        is_active=True
    )
    db_session.add(admin_user)
    await db_session.commit()
    
    # Login
    response = await client.post("/token", data={"username": "superadmin", "password": "admin123"})
    return response.json()["access_token"]

@pytest_asyncio.fixture
async def regular_user_token(db_session, client):
    from models import User
    from auth import get_password_hash
    
    user = User(
        username="user",
        hashed_password=get_password_hash("user123"),
        email="user@test.com",
        first_name="Normal",
        last_name="User",
        phone_number="111",
        is_admin=False,
        is_super_admin=False,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    response = await client.post("/token", data={"username": "user", "password": "user123"})
    return response.json()["access_token"]
