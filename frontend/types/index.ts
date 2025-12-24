export interface Category {
    id: number
    name: string
}

export interface Brand {
    id: number
    name: string
    logo_url?: string
}

export interface Product {
    id: number
    name: string
    description?: string
    price: number
    stock: number
    category_id: number
    brand_id?: number
    image_url?: string
    category?: Category
    brand?: Brand
    additional_images?: string[]
    specs?: Record<string, any>
    rating?: number
    review_count?: number
}

export interface User {
    id: number
    username: string
    email?: string
    first_name?: string
    last_name?: string
    phone_number?: string
    is_active: boolean
    is_admin: boolean
    is_super_admin: boolean
}

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
    created_at: string
    items: OrderItem[]
    user_id?: number
    customer_name?: string
    customer_email?: string
    customer_phone?: string
    shipping_address?: string
    billing_address?: string
    payment_status?: string
}

export interface OrderCreate {
    items: { product_id: number; quantity: number }[]
}

export interface TokenResponse {
    access_token: string
    token_type: string
}

export interface SiteSetting {
    key: string
    value: string
}

export interface StoreLocation {
    id: number
    name: string
    address: string
    city: string
    latitude?: number
    longitude?: number
    phone?: string
}
