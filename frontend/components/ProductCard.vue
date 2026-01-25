<script setup lang="ts">
import type { Product } from '~/types'

defineProps<{
    product: Product
    showBadge?: boolean
}>()

defineEmits(['quickView'])

const { isInWishlist, toggleWishlist } = useWishlist()
const { translateLanguage } = useLanguage()
</script>

<template>
    <NuxtLink :to="product?.id ? `/product/${product.id}` : '#'" class="product-card">
        <div class="card-badge" v-if="showBadge && product.rating && product.rating >= 4.8">
            ⭐ {{ translateLanguage('common.top_rated') }}
        </div>
        
        <div class="card-image">
            <img :src="product.image_url" :alt="product.name" loading="lazy">
            
            <div class="card-actions">
                <button 
                    class="action-btn" 
                    :class="{ 'active': isInWishlist(product.id) }"
                    @click.prevent="toggleWishlist(product.id)"
                    :title="translateLanguage('pdp.add_wishlist')"
                >
                    ♥
                </button>
                <button 
                    class="action-btn" 
                    @click.prevent="$emit('quickView', product)"
                    :title="translateLanguage('pdp.quick_view')"
                >
                    👁
                </button>
            </div>
        </div>
        
        <div class="card-body">
            <span class="card-brand" v-if="product.brand">{{ product.brand.name }}</span>
            <h3 class="card-title">{{ product.name }}</h3>
            
            <div class="card-rating" v-if="product.rating">
                <span class="stars">★★★★★</span>
                <span class="rating-text">{{ product.rating }} ({{ product.review_count?.toLocaleString() }})</span>
            </div>
            
            <div class="card-footer">
                <span class="card-price">{{ product.price.toLocaleString() }} {{ translateLanguage('common.currency') }}</span>
                <span class="card-link">{{ translateLanguage('pdp.view') }} →</span>
            </div>
        </div>
    </NuxtLink>
</template>

<style scoped>
.product-card {
    background: var(--surface);
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1px solid var(--border);
    transition: all 0.3s;
    position: relative;
    display: block;
    text-decoration: none;
    color: var(--text);
}

.product-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
}

.card-badge {
    position: absolute;
    top: 1rem;
    left: 1rem;
    background: #fbbf24;
    color: #78350f;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.7rem;
    font-weight: 700;
    z-index: 10;
}

.card-image {
    height: 200px;
    padding: 1.5rem;
    background: #f8fafc;
}

.card-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    transition: transform 0.3s;
}

.product-card:hover .card-image img {
    transform: scale(1.05);
}

.card-actions {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    gap: 0.5rem;
    opacity: 0;
    transition: opacity 0.3s;
}

.product-card:hover .card-actions {
    opacity: 1;
}

.action-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: white;
    border: none;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.25rem;
    color: var(--text);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: all 0.2s;
}

.action-btn:hover {
    background: var(--primary);
    color: white;
    transform: scale(1.1);
}

.action-btn.active {
    color: #ef4444;
}

.card-body {
    padding: 1.25rem;
}

.card-brand {
    font-size: 0.7rem;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 700;
}

.card-title {
    font-size: 1rem;
    margin: 0.5rem 0;
    line-height: 1.3;
}

.card-rating {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.stars {
    color: #fbbf24;
    font-size: 0.875rem;
}

.rating-text {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-price {
    font-size: 1.25rem;
    font-weight: 700;
}

.card-link {
    color: var(--primary);
    font-weight: 600;
    font-size: 0.875rem;
}
</style>
