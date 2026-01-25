<script setup lang="ts">
import { onMounted, watch } from 'vue'
import gsap from 'gsap'

const props = defineProps<{
    isOpen: boolean
}>()

const emit = defineEmits(['close'])

const { cart, removeFromCart, updateQuantity, subtotal, itemCount } = useCart()
const { translateLanguage, locale } = useLanguage()

// Watch for open state to animate
watch(() => props.isOpen, (newVal) => {
    if (newVal) {
        document.body.style.overflow = 'hidden'
        
        gsap.to('.cart-overlay', {
            opacity: 1,
            duration: 0.3,
            display: 'block'
        })
        
        gsap.to('.cart-drawer', {
            x: 0,
            duration: 0.4,
            ease: 'power3.out'
        })
        
        // Stagger items
        gsap.from('.cart-item', {
            x: 50,
            opacity: 0,
            stagger: 0.05,
            duration: 0.4,
            delay: 0.2
        })
    } else {
        document.body.style.overflow = ''
        
        gsap.to('.cart-overlay', {
            opacity: 0,
            duration: 0.3,
            onComplete: () => {
                gsap.set('.cart-overlay', { display: 'none' })
            }
        })
        
        gsap.to('.cart-drawer', {
            x: '100%',
            duration: 0.3,
            ease: 'power3.in'
        })
    }
})

const handleClose = () => {
    emit('close')
}

const handleCheckout = () => {
    emit('close')
    navigateTo('/checkout')
}
</script>

<template>
    <div class="cart-wrapper">
        <!-- Backdrop -->
        <div class="cart-overlay" @click="handleClose"></div>
        
        <!-- Drawer -->
        <div class="cart-drawer">
            <div class="drawer-header">
                <h2>{{ translateLanguage('cart.title') }} <span class="count">({{ itemCount }})</span></h2>
                <button class="close-btn" @click="handleClose">✕</button>
            </div>
            
            <div class="drawer-content">
                <div v-if="cart.length === 0" class="empty-state">
                    <span class="empty-icon">🛍️</span>
                    <p>{{ translateLanguage('cart.empty') }}</p>
                    <button class="btn btn-outline" @click="handleClose">{{ translateLanguage('confirmation.continue_shopping') }}</button>
                </div>
                
                <div v-else class="cart-items">
                    <div v-for="item in cart" :key="item.product.id" class="cart-item">
                        <div class="item-image">
                            <img :src="item.product.image_url" :alt="item.product.name">
                        </div>
                        <div class="item-details">
                            <div class="item-header">
                                <h3>{{ item.product.name }}</h3>
                                <button class="remove-btn" @click="removeFromCart(item.product.id)">✕</button>
                            </div>
                            <p class="price">{{ item.product.price.toLocaleString() }} {{ translateLanguage('common.currency') }}</p>
                            <div class="item-controls">
                                <div class="qty-control">
                                    <button @click="updateQuantity(item.product.id, item.quantity - 1)">−</button>
                                    <span>{{ item.quantity }}</span>
                                    <button @click="updateQuantity(item.product.id, item.quantity + 1)">+</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="drawer-footer" v-if="cart.length > 0">
                <div class="subtotal">
                    <span>{{ translateLanguage('common.total') }}</span>
                    <span class="amount">{{ subtotal.toLocaleString() }} {{ translateLanguage('common.currency') }}</span>
                </div>
                <p class="shipping-hint">{{ translateLanguage('cart.shipping_hint') }}</p>
                <button class="btn btn-primary btn-block checkout-btn" @click="handleCheckout">
                    {{ translateLanguage('cart.checkout') }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.cart-wrapper {
    position: relative;
    z-index: 9999;
}

.cart-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
    display: none;
    opacity: 0;
}

.cart-drawer {
    position: fixed;
    top: 0;
    right: 0;
    width: 100%;
    max-width: 450px;
    height: 100vh;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    box-shadow: -10px 0 30px rgba(0, 0, 0, 0.1);
    transform: translateX(100%);
    display: flex;
    flex-direction: column;
}

.drawer-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.drawer-header h2 {
    font-size: 1.25rem;
    font-weight: 700;
}

.count {
    color: var(--text-muted);
    font-weight: 500;
    font-size: 1rem;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.5rem;
    line-height: 1;
    color: var(--text-muted);
    transition: color 0.2s;
}

.close-btn:hover {
    color: var(--text);
}

.drawer-content {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
}

.empty-state {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: var(--text-muted);
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.empty-state p {
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
}

.cart-items {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.cart-item {
    display: flex;
    gap: 1rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}

.item-image {
    width: 80px;
    height: 80px;
    background: #f8fafc;
    border-radius: var(--radius);
    padding: 0.5rem;
}

.item-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.item-details {
    flex: 1;
}

.item-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.25rem;
}

.item-header h3 {
    font-size: 1rem;
    font-weight: 600;
    line-height: 1.3;
}

.remove-btn {
    background: none;
    border: none;
    color: #ef4444;
    cursor: pointer;
    padding: 0.25rem;
    font-size: 1.1rem;
    opacity: 0.5;
    transition: opacity 0.2s;
}

.remove-btn:hover {
    opacity: 1;
}

.price {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-bottom: 0.75rem;
}

.qty-control {
    display: inline-flex;
    align-items: center;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.25rem;
}

.qty-control button {
    width: 24px;
    height: 24px;
    background: var(--surface);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}

.qty-control button:hover {
    background: #f1f5f9;
}

.qty-control span {
    width: 32px;
    text-align: center;
    font-size: 0.9rem;
    font-weight: 500;
}

.drawer-footer {
    padding: 1.5rem;
    background: var(--surface);
    border-top: 1px solid var(--border);
}

.subtotal {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
    font-weight: 600;
}

.shipping-hint {
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}

.checkout-btn {
    width: 100%;
    padding: 1rem;
    font-size: 1.1rem;
}

.btn-block {
    display: block;
    width: 100%;
}
</style>
