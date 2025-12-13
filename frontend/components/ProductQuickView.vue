<script setup lang="ts">

const props = defineProps<{
    product: any
    isOpen: boolean
}>()

const emit = defineEmits(['close'])

const { addToCart } = useCart()
const { isInWishlist, toggleWishlist } = useWishlist()

const handleAddToCart = () => {
    addToCart(props.product)
    emit('close')
}
</script>

<template>
    <div v-if="isOpen" class="quick-view-overlay" @click.self="$emit('close')">
        <div class="quick-view-modal">
            <button class="close-btn" @click="$emit('close')">×</button>
            
            <div class="modal-content">
                <div class="product-image">
                    <img :src="product.image_url" :alt="product.name">
                </div>
                
                <div class="product-details">
                    <h2 class="text-2xl font-bold mb-2">{{ product.name }}</h2>
                    <p class="text-primary text-xl font-bold mb-4">${{ product.price }}</p>
                    
                    <p class="text-gray-600 mb-6">{{ product.description || 'No description available.' }}</p>
                    
                    <div class="actions">
                        <button class="btn btn-primary flex-1" @click="handleAddToCart">
                            Add to Cart
                        </button>
                        <button 
                            class="btn btn-outline w-12 flex justify-center items-center"
                            :class="{ 'text-red-500 border-red-500': isInWishlist(product.id) }"
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
