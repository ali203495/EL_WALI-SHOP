<script setup lang="ts">
import gsap from 'gsap'

useHead({
    title: 'Checkout | LUXE.TECH',
    meta: [
        { name: 'robots', content: 'noindex' }
    ]
})

const { cart, subtotal, tax, total, clearCart } = useCart()
const api = useApi()
const router = useRouter()

const loading = ref(false)
const processingStep = ref(0) // 0: input, 1: processing, 2: success

const form = reactive({
    email: '',
    firstName: '',
    lastName: '',
    address: '',
    city: '',
    country: 'US',
    zip: '',
    cardName: '',
    cardNumber: '',
    expDate: '',
    cvc: ''
})

const errors = reactive({
    email: '',
    firstName: '',
    lastName: '',
    address: '',
    city: '',
    zip: '',
    cardNumber: '',
    cvc: ''
})

const validateForm = () => {
    let isValid = true;
    // Reset errors
    (Object.keys(errors) as Array<keyof typeof errors>).forEach((key) => {
        errors[key] = ''
    })

    if (!form.email.includes('@')) { errors.email = 'Valid email required'; isValid = false }
    if (!form.firstName) { errors.firstName = 'Required'; isValid = false }
    if (!form.lastName) { errors.lastName = 'Required'; isValid = false }
    if (!form.address) { errors.address = 'Required'; isValid = false }
    if (!form.city) { errors.city = 'Required'; isValid = false }
    if (!form.zip) { errors.zip = 'Required'; isValid = false }
    if (form.cardNumber.length < 16) { errors.cardNumber = 'Invalid number'; isValid = false }
    if (form.cvc.length < 3) { errors.cvc = 'Invalid CVC'; isValid = false }

    return isValid
}

const handlePlaceOrder = async () => {
    if (!validateForm()) {
        // Shake form animation
        gsap.to('.checkout-form', { x: [-10, 10, -10, 10, 0], duration: 0.4 } as any)
        return
    }

    loading.value = true
    processingStep.value = 1
    
    try {
        // Simulate processing payment
        await new Promise(resolve => setTimeout(resolve, 2000))

        const orderItems = cart.value.map(item => ({
            product_id: item.product.id,
            quantity: item.quantity
        }))

        // Create order via API
        const order = await api.createOrder({ 
            items: orderItems,
            // Pass customer info if API supported it, simplified for now
        })

        clearCart()
        
        // Navigate to confirmation with Order ID
        router.push({
            path: '/confirmation',
            query: { orderId: order.id }
        })

    } catch (e) {
        alert('Failed to place order. Please try again.')
        loading.value = false
        processingStep.value = 0
    }
}

onMounted(() => {
    // Redirect if cart empty
    if (cart.value.length === 0) {
        navigateTo('/catalog')
        return
    }

    gsap.from('.checkout-container', {
        opacity: 0,
        duration: 0.6
    })
    
    gsap.from('.form-section', {
        y: 30,
        opacity: 0,
        duration: 0.6,
        delay: 0.2
    })
    
    gsap.from('.summary-section', {
        y: 30,
        opacity: 0,
        duration: 0.6,
        delay: 0.4
    })
})
</script>

<template>
    <div class="checkout-page">
        <div class="checkout-header">
            <div class="container">
                <NuxtLink to="/" class="logo">LUXE<span class="highlight">.TECH</span></NuxtLink>
            </div>
        </div>

        <div class="container checkout-container">
            <!-- Left Column: Forms -->
            <div class="form-section">
                <!-- Contact Info -->
                <section class="section-block">
                    <h2>Contact Information</h2>
                    <div class="form-group">
                        <label>Email Address</label>
                        <input 
                            v-model="form.email" 
                            type="email" 
                            class="input-field" 
                            :class="{ error: errors.email }"
                            placeholder="you@email.com"
                        >
                        <span class="error-msg" v-if="errors.email">{{ errors.email }}</span>
                    </div>
                </section>

                <!-- Shipping Address -->
                <section class="section-block">
                    <h2>Shipping Address</h2>
                    <div class="form-row">
                        <div class="form-group">
                            <label>First Name</label>
                            <input v-model="form.firstName" type="text" class="input-field" :class="{ error: errors.firstName }">
                        </div>
                        <div class="form-group">
                            <label>Last Name</label>
                            <input v-model="form.lastName" type="text" class="input-field" :class="{ error: errors.lastName }">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Address</label>
                        <input v-model="form.address" type="text" class="input-field" :class="{ error: errors.address }" placeholder="123 Main St">
                    </div>
                    <div class="form-row three-col">
                        <div class="form-group">
                            <label>City</label>
                            <input v-model="form.city" type="text" class="input-field" :class="{ error: errors.city }">
                        </div>
                        <div class="form-group">
                            <label>Country</label>
                            <select v-model="form.country" class="input-field select-field">
                                <option value="US">United States</option>
                                <option value="CA">Canada</option>
                                <option value="UK">United Kingdom</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>ZIP / Postal</label>
                            <input v-model="form.zip" type="text" class="input-field" :class="{ error: errors.zip }">
                        </div>
                    </div>
                </section>

                 <!-- Payment (Mock) -->
                <section class="section-block">
                    <h2>Payment Method</h2>
                    <div class="credit-card-mock">
                        <div class="form-group">
                            <label>Card Number</label>
                            <div class="input-with-icon">
                                <span class="input-icon">💳</span>
                                <input v-model="form.cardNumber" type="text" class="input-field" :class="{ error: errors.cardNumber }" placeholder="0000 0000 0000 0000" maxlength="19">
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>Name on Card</label>
                                <input v-model="form.cardName" type="text" class="input-field" placeholder="John Doe">
                            </div>
                            <div class="form-group small">
                                <label>Exp</label>
                                <input v-model="form.expDate" type="text" class="input-field" placeholder="MM/YY" maxlength="5">
                            </div>
                            <div class="form-group small">
                                <label>CVC</label>
                                <input v-model="form.cvc" type="text" class="input-field" :class="{ error: errors.cvc }" placeholder="123" maxlength="4">
                            </div>
                        </div>
                    </div>
                    <p class="secure-note">🔒 Payments are secure and encrypted.</p>
                </section>

                <button class="btn btn-primary btn-lg place-order-btn mobile-only" @click="handlePlaceOrder" :disabled="loading">
                    {{ loading ? 'Processing...' : `Pay $${total.toFixed(2)}` }}
                </button>
            </div>

            <!-- Right Column: Summary -->
            <div class="summary-section">
                <div class="summary-card">
                    <h2>Order Summary</h2>
                    
                    <div class="summary-items">
                        <div v-for="item in cart" :key="item.product.id" class="summary-item">
                            <div class="item-img-wrapper">
                                <img :src="item.product.image_url" :alt="item.product.name">
                                <span class="item-qty-badge">{{ item.quantity }}</span>
                            </div>
                            <div class="item-info">
                                <span>{{ item.product.name }}</span>
                            </div>
                            <span class="item-price">${{ (item.product.price * item.quantity).toLocaleString() }}</span>
                        </div>
                    </div>

                    <div class="summary-totals">
                        <div class="total-row">
                            <span>Subtotal</span>
                            <span>${{ subtotal.toFixed(2) }}</span>
                        </div>
                        <div class="total-row">
                            <span>Shipping</span>
                            <span>Free</span>
                        </div>
                        <div class="total-row">
                            <span>Tax (8%)</span>
                            <span>${{ tax.toFixed(2) }}</span>
                        </div>
                        <div class="total-row grand-total">
                            <span>Total</span>
                            <span><span class="currency">USD</span> ${{ total.toFixed(2) }}</span>
                        </div>
                    </div>

                    <button class="btn btn-primary btn-lg place-order-btn desktop-only" @click="handlePlaceOrder" :disabled="loading">
                        <span v-if="loading" class="spinner"></span>
                        {{ loading ? 'Processing...' : `Pay $${total.toFixed(2)}` }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.checkout-page {
    min-height: 100vh;
    background: #f8fafc;
    padding-bottom: 4rem;
}

.checkout-header {
    background: white;
    padding: 1.5rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 3rem;
}

.logo {
    font-size: 1.5rem;
    font-weight: 800;
    text-decoration: none;
    color: var(--text);
}

.highlight { color: var(--primary); }

.checkout-container {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 4rem;
    max-width: 1100px;
}

/* Forms */
.section-block {
    background: white;
    padding: 2rem;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    margin-bottom: 2rem;
}

.section-block h2 {
    font-size: 1.25rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.form-row.three-col {
    grid-template-columns: 1.5fr 1fr 1fr;
}

.form-group {
    margin-bottom: 1.25rem;
}

.form-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.input-field {
    width: 100%;
    padding: 0.875rem;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-size: 1rem;
    transition: all 0.2s;
}

.input-field:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px var(--primary-light);
}

.input-field.error {
    border-color: #ef4444;
    background: #fef2f2;
}

.error-msg {
    color: #ef4444;
    font-size: 0.75rem;
    margin-top: 0.25rem;
    display: block;
}

.select-field {
    background-color: white;
}

/* Payment */
.credit-card-mock {
    background: #f8fafc;
    padding: 1.5rem;
    border-radius: var(--radius);
    border: 1px solid var(--border);
}

.input-with-icon {
    position: relative;
}

.input-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.2rem;
}

.input-with-icon .input-field {
    padding-left: 3rem;
}

.secure-note {
    margin-top: 1rem;
    font-size: 0.875rem;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Summary */
.summary-card {
    background: white;
    padding: 2rem;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    position: sticky;
    top: 2rem;
}

.summary-card h2 {
    font-size: 1.25rem;
    margin-bottom: 1.5rem;
}

.summary-items {
    margin-bottom: 2rem;
    max-height: 400px;
    overflow-y: auto;
}

.summary-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.item-img-wrapper {
    position: relative;
    width: 64px;
    height: 64px;
    background: #f8fafc;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    padding: 0.25rem;
}

.item-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.item-qty-badge {
    position: absolute;
    top: -8px;
    right: -8px;
    background: #64748b;
    color: white;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.item-info {
    flex: 1;
    font-size: 0.9375rem;
    font-weight: 500;
}

.item-price {
    font-weight: 600;
    color: var(--text-muted);
}

.summary-totals {
    border-top: 1px solid var(--border);
    padding-top: 1.5rem;
}

.total-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.75rem;
    color: var(--text-muted);
}

.total-row.grand-total {
    color: var(--text);
    font-size: 1.5rem;
    font-weight: 800;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px dashed var(--border);
    align-items: center;
}

.currency {
    font-size: 0.875rem;
    color: var(--text-muted);
    font-weight: 500;
    margin-right: 0.25rem;
}

.place-order-btn {
    width: 100%;
    margin-top: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
}

.spinner {
    width: 1.2rem;
    height: 1.2rem;
    border: 2px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.mobile-only { display: none; }

@media (max-width: 900px) {
    .checkout-container {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
    
    .summary-section {
        order: -1; /* Summary first on mobile */
    }
    
    .desktop-only { display: none; }
    .mobile-only { display: block; }
}

@media (max-width: 600px) {
    .form-row, .form-row.three-col {
        grid-template-columns: 1fr;
    }
}
</style>
