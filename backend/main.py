from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Annotated, List
from datetime import timedelta
import contextlib
import shutil
import os
import uuid

from database import get_db, engine, Base
from models import User, Brand, StoreLocation, Category, Product, Order, OrderItem, Wishlist, SiteSetting
from schemas import (
    UserCreate, UserResponse, Token, UserPasswordUpdate, UserUpdate, UserLogin,
    CategoryCreate, CategoryResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    BrandCreate, BrandResponse, StoreLocationCreate, StoreLocationResponse, ProductResponseFull,
    SiteSettingCreate, SiteSettingResponse,
    PasswordResetRequest, PasswordResetConfirm,
    WishlistResponse, WishlistCreate,
    OrderCreate, OrderResponse
)
from auth import get_password_hash, verify_password, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="POS & Admin API", version="1.0.0", lifespan=lifespan)

# Mount static files for uploads
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://192.168.240.1:3000",
    "http://192.168.240.1:3001",
    "*", # Allow all for development testing across LAN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Return URL (assuming served via /static)
    # Using absolute URL helps frontend preview immediately if needed, 
    # but relative path is more portable. 
    # Given proxy setup: /api/static/... -> backend/uploads/...
    # But wait, app.mount("/static") means url is /static/...
    # Frontend via proxy /api -> backend. So /api/static/...
    return {"url": f"http://localhost:8000/static/{unique_filename}"}

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/verify-password")
async def verify_user_password(
    body: UserPasswordUpdate, 
    current_user: User = Depends(get_current_active_user)
):
    if not verify_password(body.password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"message": "Password verified"}

@app.post("/auth/verify-super-credentials")
async def verify_super_credentials(
    body: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    # Check if user exists
    print(f"DEBUG LOGIN ATTEMPT: username='{body.username}'")
    result = await db.execute(select(User).where(User.username == body.username))
    user = result.scalars().first()
    
    if not user:
        print("DEBUG FAILURE: User not found")
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(body.password, user.hashed_password):
        print("DEBUG FAILURE: Password verification failed")
        raise HTTPException(status_code=400, detail="Invalid credentials")
        
    if not user.is_super_admin:
        print(f"DEBUG FAILURE: User {user.username} is not super admin")
        raise HTTPException(status_code=403, detail="User is not a Super Admin")
        
    print("DEBUG SUCCESS: Verified!")
    return {"message": "Verified", "is_super_admin": True}

@app.post("/users/", response_model=UserResponse)
async def create_user(
    user: UserCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Only super admin can create users
    # Only super admin can create users
    if not current_user.is_super_admin:
        raise HTTPException(status_code=403, detail="Only the super admin can create users")

    result = await db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pwd = get_password_hash(user.password)
    db_user = User(
        username=user.username, 
        hashed_password=hashed_pwd, 
        is_admin=user.is_admin,
        is_super_admin=user.is_super_admin,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Only super admin can edit users
    if current_user.username != "Abdelaali" and not current_user.is_admin:
         # Allow admins to edit? The requirement said "add admin", implying admins can manage users.
         # For safety, sticking to super admin or maybe allow self-edit?
         # "I want you to make it so that when someone wants to add an admin..."
         # Assuming 'someone' means an existing admin.
         # Let's relax this to allow admins to edit, or at least the super admin key.
         pass
    
    # Only super admin can edit users OR user editing themselves
    is_self = current_user.id == user_id
    is_super = current_user.is_super_admin
    
    if not is_super and not is_self:
        raise HTTPException(status_code=403, detail="Not authorized to edit this user")

    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # If updating username, check for uniqueness
    if user_update.username and user_update.username != db_user.username:
        existing_check = await db.execute(select(User).where(User.username == user_update.username))
        if existing_check.scalars().first():
            raise HTTPException(status_code=400, detail="Username already registered")
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@app.get("/users/", response_model=List[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not current_user.is_super_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await db.execute(select(User))
    return result.scalars().all()

@app.put("/users/{user_id}/password", response_model=UserResponse)
async def update_user_password(
    user_id: int, 
    password_update: UserPasswordUpdate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_super_admin:
        raise HTTPException(status_code=403, detail="Only the super admin can set passwords")
    
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db_user.hashed_password = get_password_hash(password_update.password)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    # Only super admin can delete users
    if not current_user.is_super_admin:
        raise HTTPException(status_code=403, detail="Only the super admin can delete users")
    
    # Prevent self-deletion
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted successfully"}

# --- Password Recovery ---
import random
import string
from datetime import datetime, timezone

@app.post("/auth/forgot-password")
async def forgot_password(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import update
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalars().first()
    
    if not user:
        # Don't reveal if user exists
        return {"message": "If the email exists, a code has been sent."}
    
    # Generate 6-digit code
    code = ''.join(random.choices(string.digits, k=6))
    
    # Use explicit update to avoid Greenlet/ORM issues
    stmt = (
        update(User)
        .where(User.email == request.email)
        .values(
            reset_token=code, 
            reset_token_expiry=datetime.now(timezone.utc) + timedelta(minutes=15)
        )
    )
    await db.execute(stmt)
    await db.commit()
    
    # In a real app, send email/SMS here
    print(f"DEBUG: Password reset code for {request.email}: {code}")
    
    return {"message": "If the email exists, a code has been sent."}

@app.post("/auth/reset-password")
async def reset_password(
    request: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid request")
        
    if not user.reset_token or user.reset_token != request.code:
        raise HTTPException(status_code=400, detail="Invalid code")
        
    if not user.reset_token_expiry or user.reset_token_expiry.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Code expired")
        
    # Reset password
    user.hashed_password = get_password_hash(request.new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    
    await db.commit()
    return {"message": "Password updated successfully"}

@app.get("/")
async def root():
    return {"message": "POS & Admin API is running"}

# --- Categories ---

@app.post("/categories/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Only admins/users can create (for now all active users)
    db_category = Category(name=category.name)
    db.add(db_category)
    try:
        await db.commit()
        await db.refresh(db_category)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists")
    return db_category

@app.get("/categories/", response_model=List[CategoryResponse])
async def read_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()

@app.delete("/categories/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    db_category = result.scalars().first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    await db.delete(db_category)
    await db.commit()
    return {"message": "Category deleted successfully"}

# --- Products ---

@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    
    # Re-fetch with eager loading for response
    # We must start a new query to avoid Greenlet issues with the committed instance
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.id == db_product.id)
    )
    fetched_product = result.scalars().first()
    return fetched_product

@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_update: ProductUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    await db.commit()
    
    # Re-fetch with eager loading
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.id == product_id)
    )
    fetched_product = result.scalars().first()
    return fetched_product

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if product is used in any orders
    # from models import OrderItem # Already imported at top level
    result_usage = await db.execute(select(OrderItem).where(OrderItem.product_id == product_id).limit(1))
    if result_usage.scalars().first():
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete product because it is part of existing orders. Consider hiding it (setting Stock to 0) instead."
        )

    await db.delete(db_product)
    await db.commit()
    return {"message": "Product deleted successfully"}

@app.get("/products/", response_model=List[ProductResponse])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Perform a join so we can access category data if needed
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()

@app.get("/products/{product_id}", response_model=ProductResponse)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.id == product_id)
    )
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/orders/", response_model=List[OrderResponse])
async def read_orders(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(Order).options(selectinload(Order.items))
    
    # If not admin, filter by user
    if not current_user.is_admin:
        query = query.where(Order.user_id == current_user.id)
        
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

# --- Orders / POS ---

@app.post("/orders/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate, 
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Try to get user from token if present
    user_id = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        from auth import verify_token_data
        username = verify_token_data(token)
        if username:
             result = await db.execute(select(User).where(User.username == username))
             user = result.scalars().first()
             if user:
                 user_id = user.id

    # 1. Validate products and calculate total
    total_amount = 0.0
    db_order = Order(status="completed", user_id=user_id)
    db.add(db_order)
    await db.flush() # get ID

    for item in order.items:
        result = await db.execute(select(Product).where(Product.id == item.product_id))
        product = result.scalars().first()
        if not product:
            await db.rollback()
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        if product.stock < item.quantity:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")
        
        # Deduct stock
        product.stock -= item.quantity
        
        # Add order item
        line_total = product.price * item.quantity
        total_amount += line_total
        
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_time=product.price
        )
        db.add(db_item)

    db_order.total_amount = total_amount
    
    # Cache ID to prevent MissingGreenlet on re-access after commit
    order_id = db_order.id
    
    await db.commit()
    
    # Re-fetch order with items eagerly loaded to satisfy Pydantic schema
    # preventing MissingGreenlet error
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )
    return result.scalars().first()

# --- Brands ---

@app.get("/brands/", response_model=List[BrandResponse])
async def read_brands(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand))
    return result.scalars().all()

# --- Site Settings (CMS) ---

@app.get("/settings/", response_model=List[SiteSettingResponse])
async def read_settings(db: AsyncSession = Depends(get_db)):
    # from models import SiteSetting # Already imported
    result = await db.execute(select(SiteSetting))
    return result.scalars().all()

@app.put("/settings/", response_model=List[SiteSettingResponse])
async def update_settings(settings: List[SiteSettingCreate], db: AsyncSession = Depends(get_db)):
    # from models import SiteSetting
    
    # Upsert logic
    for setting in settings:
        result = await db.execute(select(SiteSetting).where(SiteSetting.key == setting.key))
        db_setting = result.scalars().first()
        if db_setting:
            db_setting.value = setting.value
        else:
            new_setting = SiteSetting(key=setting.key, value=setting.value)
            db.add(new_setting)
    
    await db.commit()
    
    # Return all settings
    result = await db.execute(select(SiteSetting))
    return result.scalars().all()

@app.post("/brands/", response_model=BrandResponse)
async def create_brand(brand: BrandResponse, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_brand = Brand(name=brand.name, logo_url=brand.logo_url)
    db.add(db_brand)
    await db.commit()
    await db.refresh(db_brand)
    return db_brand

@app.delete("/brands/{brand_id}")
async def delete_brand(brand_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    result = await db.execute(select(Brand).where(Brand.id == brand_id))
    db_brand = result.scalars().first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    await db.delete(db_brand)
    await db.commit()
    return {"message": "Brand deleted successfully"}

# --- Store Locations ---

@app.get("/stores/", response_model=List[StoreLocationResponse])
async def read_stores(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StoreLocation))
    return result.scalars().all()

@app.post("/stores/", response_model=StoreLocationResponse)
async def create_store(store: StoreLocationCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_store = StoreLocation(**store.model_dump())
    db.add(db_store)
    await db.commit()
    await db.refresh(db_store)
    return db_store

@app.delete("/stores/{store_id}")
async def delete_store(store_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    result = await db.execute(select(StoreLocation).where(StoreLocation.id == store_id))
    db_store = result.scalars().first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    await db.delete(db_store)
    await db.commit()
    return {"message": "Store deleted successfully"}

# --- Enhanced Products with Brand (for Catalog) ---

@app.get("/catalog/", response_model=List[ProductResponseFull])
async def read_catalog(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Eager load brand and category for rich responses
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.brand), selectinload(Product.category))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@app.get("/catalog/{product_id}", response_model=ProductResponseFull)
async def read_catalog_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.brand), selectinload(Product.category))
    )
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# --- Wishlist ---

@app.get("/wishlist/", response_model=List[WishlistResponse])
async def read_wishlist(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    result = await db.execute(
        select(Wishlist)
        .where(Wishlist.user_id == current_user.id)
        .options(selectinload(Wishlist.product))
    )
    return result.scalars().all()

@app.post("/wishlist/", response_model=WishlistResponse)
async def add_to_wishlist(
    item: WishlistCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    # Check if already exists
    result = await db.execute(
        select(Wishlist)
        .where(Wishlist.user_id == current_user.id)
        .where(Wishlist.product_id == item.product_id)
    )
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Product already in wishlist")

    db_wishlist = Wishlist(user_id=current_user.id, product_id=item.product_id)
    db.add(db_wishlist)
    await db.commit()
    
    # Refresh to get product relationship
    result = await db.execute(
        select(Wishlist)
        .where(Wishlist.id == db_wishlist.id)
        .options(selectinload(Wishlist.product))
    )
    return result.scalars().first()

@app.delete("/wishlist/{product_id}")
async def remove_from_wishlist(
    product_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(Wishlist)
        .where(Wishlist.user_id == current_user.id)
        .where(Wishlist.product_id == product_id)
    )
    db_item = result.scalars().first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found in wishlist")
        
    await db.delete(db_item)
    await db.commit()
    return {"message": "Removed from wishlist"}
