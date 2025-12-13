<script setup lang="ts">
import { ref, computed } from 'vue'
import gsap from 'gsap'

definePageMeta({
    layout: false
})

const api = useApi()
const cart = ref<any[]>([])
const checkoutLoading = ref(false)
const orderSuccess = ref(false)

// Fetch products from catalog API
const { data: products } = await api.getProducts()

const addToCart = (product: any) => {
    const existing = cart.value.find(item => item.product.id === product.id)
    
    if (existing) {
        existing.quantity++
        // Pulse animation on quantity
        gsap.fromTo(`#qty-${product.id}`, 
            { scale: 1.3, color: '#4f46e5' }, 
            { scale: 1, color: '#0f172a', duration: 0.3 }
        )
    } else {
        cart.value.push({ product, quantity: 1 })
        
        nextTick(() => {
            gsap.from(`#cart-item-${product.id}`, {
                x: -30,
                opacity: 0,
                duration: 0.4,
                ease: 'back.out(1.7)'
            })
        })
    }

    // Product card feedback
    const el = document.getElementById(`product-${product.id}`)
    if (el) {
        gsap.to(el, {
            scale: 0.95,
            duration: 0.1,
            yoyo: true,
            repeat: 1,
            ease: 'power2.inOut'
        })
    }
}

const removeFromCart = (productId: number) => {
    const index = cart.value.findIndex(item => item.product.id === productId)
    if (index > -1) {
        gsap.to(`#cart-item-${productId}`, {
            x: 50,
            opacity: 0,
            duration: 0.3,
            onComplete: () => {
                cart.value.splice(index, 1)
            }
        })
    }
}

const updateQuantity = (productId: number, delta: number) => {
    const item = cart.value.find(i => i.product.id === productId)
    if (item) {
        item.quantity += delta
        if (item.quantity <= 0) {
            removeFromCart(productId)
        }
    }
}

const subtotal = computed(() => {
    return cart.value.reduce((sum, item) => sum + (item.product.price * item.quantity), 0)
})

const tax = computed(() => subtotal.value * 0.08)
const total = computed(() => subtotal.value + tax.value)

const checkout = async () => {
    if (cart.value.length === 0) return
    
    checkoutLoading.value = true
    const orderItems = cart.value.map(item => ({
        product_id: item.product.id,
        quantity: item.quantity
    }))
    
    try {
        await api.createOrder({ items: orderItems })
        orderSuccess.value = true
        cart.value = []
        
        setTimeout(() => {
            orderSuccess.value = false
        }, 3000)
    } catch (e) {
        alert('Error placing order')
    } finally {
        checkoutLoading.value = false
    }
}

const clearCart = () => {
    gsap.to('.cart-item', {
        x: 50,
        opacity: 0,
        stagger: 0.05,
        duration: 0.2,
        onComplete: () => {
            cart.value = []
        }
    })
}
</script>

<template>
    <div class="pos-container">
        <!-- Product Grid -->
        <div class="products-area">
            <div class="pos-header">
                <h1>Point of Sale</h1>
                <NuxtLink to="/admin" class="btn btn-outline btn-sm">← Back to Admin</NuxtLink>
            </div>
            
            <div class="products-grid">
                <div 
                    v-for="product in products" 
                    :key="product.id" 
                    :id="`product-${product.id}`"
                    class="product-tile" 
                    @click="addToCart(product)"
                >
                    <img :src="product.image_url" :alt="product.name" class="product-image">
                    <div class="product-details">
                        <span class="product-brand" v-if="product.brand">{{ product.brand.name }}</span>
                        <h3>{{ product.name }}</h3>
                        <div class="product-meta">
                            <span class="product-price">${{ product.price }}</span>
                            <span class="product-stock" :class="{ low: product.stock < 20 }">
                                {{ product.stock }} left
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Cart Sidebar -->
        <div class="cart-panel">
            <div class="cart-header">
                <h2>Current Order</h2>
                <button v-if="cart.length > 0" @click="clearCart" class="clear-btn">Clear All</button>
            </div>
            
            <div class="cart-items">
                <div v-if="cart.length === 0" class="empty-cart">
                    <span class="empty-icon">🛒</span>
                    <p>Cart is empty</p>
                    <p class="hint">Click products to add them</p>
                </div>
                
                <div 
                    v-for="item in cart" 
                    :key="item.product.id" 
                    :id="`cart-item-${item.product.id}`"
                    class="cart-item"
                >
                    <img :src="item.product.image_url" class="cart-thumb">
                    <div class="cart-item-info">
                        <span class="cart-item-name">{{ item.product.name }}</span>
                        <span class="cart-item-price">${{ (item.product.price * item.quantity).toFixed(2) }}</span>
                    </div>
                    <div class="quantity-controls">
                        <button @click.stop="updateQuantity(item.product.id, -1)">−</button>
                        <span :id="`qty-${item.product.id}`">{{ item.quantity }}</span>
                        <button @click.stop="updateQuantity(item.product.id, 1)">+</button>
                    </div>
                </div>
            </div>
            
            <div class="cart-summary">
                <div class="summary-row">
                    <span>Subtotal</span>
                    <span>${{ subtotal.toFixed(2) }}</span>
                </div>
                <div class="summary-row">
                    <span>Tax (8%)</span>
                    <span>${{ tax.toFixed(2) }}</span>
                </div>
                <div class="summary-row total">
                    <span>Total</span>
                    <span>${{ total.toFixed(2) }}</span>
                </div>
                
                <button 
                    class="checkout-btn" 
                    :disabled="cart.length === 0 || checkoutLoading"
                    @click="checkout"
                >
                    <span v-if="checkoutLoading">Processing...</span>
                    <span v-else-if="orderSuccess">✓ Order Placed!</span>
                    <span v-else>Complete Order</span>
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.pos-container {
    display: grid;
    grid-template-columns: 1fr 400px;
    height: 100vh;
    background: #0f172a;
}

.products-area {
    padding: 2rem;
    overflow-y: auto;
}

.pos-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    color: white;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
}

.product-tile {
    background: #1e293b;
    border-radius: 1rem;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.2s;
    border: 2px solid transparent;
}

.product-tile:hover {
    border-color: var(--primary);
    transform: translateY(-4px);
}

.product-tile:active {
    transform: scale(0.98);
}

.product-image {
    width: 100%;
    height: 120px;
    object-fit: cover;
    background: #0f172a;
}

.product-details {
    padding: 1rem;
    color: white;
}

.product-brand {
    font-size: 0.7rem;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

.product-details h3 {
    font-size: 0.9rem;
    margin: 0.25rem 0 0.5rem;
    line-height: 1.3;
}

.product-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.product-price {
    font-size: 1.1rem;
    font-weight: 700;
    color: #22c55e;
}

.product-stock {
    font-size: 0.75rem;
    color: #64748b;
}

.product-stock.low {
    color: #f59e0b;
}

/* Cart Panel */
.cart-panel {
    background: var(--surface);
    display: flex;
    flex-direction: column;
}

.cart-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.clear-btn {
    background: none;
    border: none;
    color: #ef4444;
    font-size: 0.875rem;
    cursor: pointer;
}

.cart-items {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
}

.empty-cart {
    text-align: center;
    padding: 3rem 1rem;
    color: #94a3b8;
}

.empty-icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 1rem;
}

.hint {
    font-size: 0.875rem;
    margin-top: 0.5rem;
}

.cart-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: #f8fafc;
    border-radius: 0.75rem;
    margin-bottom: 0.75rem;
}

.cart-thumb {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 0.5rem;
}

.cart-item-info {
    flex: 1;
}

.cart-item-name {
    display: block;
    font-weight: 600;
    font-size: 0.875rem;
    margin-bottom: 0.25rem;
}

.cart-item-price {
    color: var(--primary);
    font-weight: 700;
}

.quantity-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.quantity-controls button {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: 1px solid var(--border);
    background: var(--surface);
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
}

.quantity-controls button:hover {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.quantity-controls span {
    min-width: 24px;
    text-align: center;
    font-weight: 600;
}

/* Cart Summary */
.cart-summary {
    padding: 1.5rem;
    border-top: 1px solid var(--border);
    background: #f8fafc;
}

.summary-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.75rem;
    color: #64748b;
}

.summary-row.total {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    padding-top: 0.75rem;
    border-top: 1px solid var(--border);
    margin-top: 0.75rem;
}

.checkout-btn {
    width: 100%;
    padding: 1rem;
    margin-top: 1rem;
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    color: white;
    border: none;
    border-radius: 0.75rem;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
}

.checkout-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(34, 197, 94, 0.4);
}

.checkout-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style>
