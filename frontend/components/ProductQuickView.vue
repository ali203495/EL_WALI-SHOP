<script setup lang="ts">
const props = defineProps<{
    product: any
    isOpen: boolean
}>()

const emit = defineEmits(['close'])

const { addToCart } = useCart()
const { isInWishlist, toggleWishlist } = useWishlist()
const { translateLanguage } = useLanguage()

const quantity = ref(1)

const incrementQty = () => {
    if (props.product && quantity.value < (props.product.stock || 0)) {
        quantity.value++
    }
}

const decrementQty = () => {
    if (quantity.value > 1) {
        quantity.value--
    }
}

const handleAddToCart = () => {
    addToCart(props.product, quantity.value)
    emit('close')
}
</script>

<template>
    <div v-if="isOpen" class="quick-view-overlay" @click.self="emit('close')">
        <div class="quick-view-modal">
            <button class="close-btn" @click="emit('close')">×</button>
            
            <div class="modal-content">
                <div class="product-image">
                    <img :src="product.image_url" :alt="product.name">
                </div>
                
                <div class="product-details">
                    <h2 class="text-2xl font-bold mb-2">{{ product.name }}</h2>
                    <p class="text-primary text-xl font-bold mb-4">{{ product.price.toLocaleString() }} {{ translateLanguage('common.currency') }}</p>
                    
                    <p class="text-gray-600 mb-6">{{ product.description || translateLanguage('pdp.no_description') }}</p>
                    
                    <div class="qty-selector-quick" v-if="product.stock > 0">
                        <label>{{ translateLanguage('pdp.quantity') }}</label>
                        <div class="qty-controls">
                            <button class="qty-btn" @click="decrementQty" :disabled="quantity <= 1">−</button>
                            <span class="qty-value">{{ quantity }}</span>
                            <button class="qty-btn" @click="incrementQty" :disabled="quantity >= product.stock">+</button>
                        </div>
                    </div>

                    <div class="actions">
                        <button 
                            class="btn btn-primary flex-1" 
                            :disabled="product.stock <= 0"
                            @click="handleAddToCart"
                        >
                            {{ product.stock > 0 ? translateLanguage('pdp.add_to_cart') : translateLanguage('pdp.out_stock') }}
                        </button>
                        <button 
                            class="btn btn-outline w-12 flex justify-center items-center wishlist-btn"
                            :class="{ 'in-wishlist': isInWishlist(product.id) }"
                            @click="toggleWishlist(product.id)"
                        >
                            ♥
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.quick-view-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    animation: fadeIn 0.3s;
}

.quick-view-modal {
    background: white;
    border-radius: 1rem;
    width: 90%;
    max-width: 800px;
    position: relative;
    overflow: hidden;
    animation: slideUp 0.3s;
}

.close-btn {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    z-index: 10;
}

.modal-content {
    display: flex;
    flex-direction: column;
}

@media (min-width: 768px) {
    .modal-content {
        flex-direction: row;
    }
}

.product-image {
    flex: 1;
    background: #f8fafc;
    padding: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.product-image img {
    max-width: 100%;
    max-height: 300px;
    object-fit: contain;
}

.product-details {
    flex: 1;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.qty-selector-quick {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.qty-selector-quick label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
}

.qty-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.25rem;
    background: #f1f5f9;
    border-radius: 0.5rem;
    width: fit-content;
}

.qty-btn {
    width: 32px;
    height: 32px;
    border: 1px solid #e2e8f0;
    background: white;
    border-radius: 0.4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
}

.qty-btn:hover:not(:disabled) {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.qty-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.qty-value {
    font-weight: 700;
    min-width: 30px;
    text-align: center;
}

.actions {
    display: flex;
    gap: 1rem;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
</style>
