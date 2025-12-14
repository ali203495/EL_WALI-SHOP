// Product Types
export interface Brand {
    id: number
    name: string
    logo_url?: string
}

export interface Category {
    id: number
    name: string
    image_url?: string
}

export interface Product {
    id: number
    name: string
    description?: string
    price: number
    stock: number
    image_url?: string
    additional_images?: string[]
    specs?: Record<string, string>
    rating?: number
    review_count?: number
    category_id?: number
    brand_id?: number
    category?: Category
    brand?: Brand
}

// Store Types
export interface StoreLocation {
    id: number
    name: string
    address: string
    city: string
    latitude: number
    longitude: number
    phone: string
}

// Order Types
export interface OrderItem {
    id: number
    product_id: number
    quantity: number
    price_at_time: number
}

export interface Order {
    id: number
    total_amount: number
    status: string
    items: OrderItem[]
    created_at: string
}

export interface OrderCreateItem {
    product_id: number
    quantity: number
}

export interface OrderCreate {
    items: OrderCreateItem[]
}

// Auth Types
export interface User {
    id: number
    username: string
    is_active: boolean
    is_admin: boolean
    is_super_admin: boolean
}

export interface TokenResponse {
    access_token: string
    token_type: string
}

// API Response wrapper
export interface ApiError {
    detail: string
}
