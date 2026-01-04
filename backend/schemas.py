from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None

class UserCreate(UserBase):
    password: str
    email: str # Required for creation
    first_name: str # Required
    last_name: str # Required
    phone_number: str # Required
    is_admin: bool = False
    is_super_admin: bool = False

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    is_admin: bool | None = None
    is_super_admin: bool | None = None
    is_active: bool | None = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_super_admin: bool = False

    model_config = ConfigDict(from_attributes=True)

class UserPasswordUpdate(BaseModel):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    email: str
    code: str
    new_password: str



# --- Categories ---
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Products ---
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    category_id: int
    brand_id: int | None = None
    description: str | None = None
    image_url: str | None = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int | None = None
    category_id: int | None = None
    brand_id: int | None = None
    description: str | None = None
    image_url: str | None = None


class ProductResponse(ProductBase):
    id: int
    category: CategoryResponse | None = None
    model_config = ConfigDict(from_attributes=True)

# --- Orders ---
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: list[OrderItemBase]
    # Customer Details
    email: str
    firstName: str
    lastName: str
    address: str
    city: str
    country: str
    zip: str

class OrderItemResponse(OrderItemBase):
    id: int
    price_at_time: float
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    payment_method: str | None = None
    created_at: datetime
    items: list[OrderItemResponse]
    # Customer Details
    customer_email: str | None = None
    customer_first_name: str | None = None
    customer_last_name: str | None = None
    customer_address: str | None = None
    customer_city: str | None = None
    customer_country: str | None = None
    customer_zip: str | None = None
    items: list[OrderItemResponse]
    model_config = ConfigDict(from_attributes=True)

# --- Brands ---
class BrandBase(BaseModel):
    name: str
    logo_url: str | None = None

class BrandCreate(BrandBase):
    pass

class BrandResponse(BrandBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Store Locations ---
class StoreLocationBase(BaseModel):
    name: str
    address: str
    city: str
    latitude: float | None = None
    longitude: float | None = None
    phone: str | None = None

class StoreLocationCreate(StoreLocationBase):
    pass

class StoreLocationResponse(StoreLocationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Enhanced Product (with Brand) ---
class ProductResponseFull(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    stock: int
    image_url: str | None = None
    additional_images: list[str] | None = None
    specs: dict | None = None
    rating: float | None = None
    review_count: int | None = None
    category_id: int | None = None
    brand_id: int | None = None
    category: CategoryResponse | None = None
    brand: BrandResponse | None = None
    brand: BrandResponse | None = None
    model_config = ConfigDict(from_attributes=True)

class StartLocationResponse(StoreLocationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Settings ---
class SiteSettingBase(BaseModel):
    key: str
    value: str

class SiteSettingCreate(SiteSettingBase):
    pass

class SiteSettingResponse(SiteSettingBase):
    model_config = ConfigDict(from_attributes=True)

# --- Wishlist ---
from datetime import datetime

class WishlistCreate(BaseModel):
    product_id: int

class WishlistResponse(BaseModel):
    id: int
    product: ProductResponseFull
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
