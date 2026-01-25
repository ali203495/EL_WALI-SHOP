<script setup lang="ts">
import { gsap } from 'gsap'

const { translateLanguage } = useLanguage()
const { fetchWishlist, items, isLoading, removeFromWishlist } = useWishlist()
const { addToCart } = useCart()

const apiError = ref<any>(null)

onMounted(async () => {
    try {
        await fetchWishlist()
    } catch (e) {
        apiError.value = e
    }
    
    gsap.from('.wishlist-item', {
        y: 20,
        opacity: 0,
        stagger: 0.1,
        duration: 0.5
    })
})
</script>

<template>
    <div class="wishlist-page">
        <div class="container">
            <header class="page-header">
                <h1>{{ translateLanguage('wishlist.title') }}</h1>
                <p v-if="items.length > 0" class="subtitle">{{ items.length }} {{ items.length === 1 ? 'item' : 'items' }} in your set</p>
            </header>
            
            <ErrorState 
                v-if="apiError"
                :title="translateLanguage('admin.failed_load')"
                :description="translateLanguage('common.error_desc')"
                :retryable="true"
                @retry="fetchWishlist"
            />

            <div v-else-if="isLoading && items.length === 0" class="loading-wishlist">
                <Spinner size="lg" />
            </div>

            <div v-else-if="items.length === 0" class="empty-wishlist">
                <div class="empty-visual">✨</div>
                <h2>{{ translateLanguage('wishlist.empty_title') }}</h2>
                <p>{{ translateLanguage('wishlist.empty_desc') }}</p>
                <NuxtLink to="/catalog" class="btn btn-primary">{{ translateLanguage('wishlist.browse') }}</NuxtLink>
            </div>

            <div v-else class="wishlist-grid">
                <div v-for="item in items" :key="item.id" class="wishlist-card">
                    <div class="card-image">
                        <img :src="item.product.image_url" :alt="item.product.name">
                        <button class="remove-wish-btn" :title="translateLanguage('common.delete')" @click="removeFromWishlist(item.product.id)">
                            ✕
                        </button>
                    </div>
                    <div class="card-content">
                        <div class="card-info">
                            <h3>{{ item.product.name }}</h3>
                            <p class="card-price">{{ item.product.price.toLocaleString() }} {{ translateLanguage('common.currency') }}</p>
                        </div>
                        <button class="btn btn-outline btn-sm add-cart-btn" @click="addToCart(item.product)">
                            {{ translateLanguage('pdp.add_to_cart') }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.wishlist-page {
    padding-bottom: 5rem;
    min-height: 70vh;
}

.page-header {
    margin-bottom: 3rem;
    padding-top: 2rem;
}

.page-header h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.subtitle {
    color: var(--text-muted);
    font-size: 1.1rem;
}

.loading-wishlist {
    display: flex;
    justify-content: center;
    padding: 5rem 0;
}

/* Empty State */
.empty-wishlist {
    text-align: center;
    padding: 5rem 2rem;
    background: white;
    border-radius: var(--radius-lg);
    border: 1px dashed var(--border);
}

.empty-visual {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    display: block;
}

.empty-wishlist h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.empty-wishlist p {
    color: var(--text-muted);
    margin-bottom: 2rem;
    max-width: 400px;
    margin-inline: auto;
}

/* Grid */
.wishlist-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
}

.wishlist-card {
    background: white;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.wishlist-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.card-image {
    position: relative;
    height: 240px;
    background: #f8fafc;
    padding: 1.5rem;
}

.card-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    transition: transform 0.5s;
}

.wishlist-card:hover .card-image img {
    transform: scale(1.05);
}

.remove-wish-btn {
    position: absolute;
    top: 1rem;
    right: 1rem;
    width: 32px;
    height: 32px;
    background: white;
    border: 1px solid var(--border);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;
    transform: translateY(-10px);
    transition: all 0.3s;
    color: var(--text-muted);
}

.wishlist-card:hover .remove-wish-btn {
    opacity: 1;
    transform: translateY(0);
}

.remove-wish-btn:hover {
    background: #fee2e2;
    color: #dc2626;
    border-color: #fecaca;
}

.card-content {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.card-info h3 {
    font-size: 1.125rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    line-height: 1.4;
}

.card-price {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary);
}

.add-cart-btn {
    width: 100%;
    padding: 0.75rem;
    font-weight: 600;
}
</style>
