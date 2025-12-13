<script setup lang="ts">
import gsap from 'gsap'

const route = useRoute()
const config = useRuntimeConfig()

// Get initial query from URL
const searchQuery = ref((route.query.q as string) || '')

useHead({
    title: computed(() => searchQuery.value ? `Search: ${searchQuery.value}` : 'Search Products'),
    meta: [
        { name: 'robots', content: 'noindex, follow' }
    ]
})

const api = useApi()
const { data: products } = await api.getProducts()

const filteredProducts = computed(() => {
    if (!products.value) return []
    if (!searchQuery.value) return products.value
    
    const q = searchQuery.value.toLowerCase()
    return products.value.filter(p => 
        p.name.toLowerCase().includes(q) ||
        p.description?.toLowerCase().includes(q) ||
        p.brand?.name.toLowerCase().includes(q) ||
        p.category?.name.toLowerCase().includes(q)
    )
})

const handleSearch = () => {
    // Update URL with search query
    navigateTo({ 
        path: '/search', 
        query: { q: searchQuery.value } 
    })
}

onMounted(() => {
    gsap.from('.result-card', {
        y: 30,
        opacity: 0,
        stagger: 0.05,
        duration: 0.5
    })
})
</script>

<template>
    <div class="search-page">
        <div class="container">
            <!-- Search Header -->
            <div class="search-header">
                <h1>Search Results</h1>
                <form @submit.prevent="handleSearch" class="search-form">
                    <input 
                        v-model="searchQuery" 
                        type="text" 
                        placeholder="Search products, brands, categories..."
                        class="input-field search-input"
                    >
                    <button type="submit" class="btn btn-primary">Search</button>
                </form>
            </div>

            <!-- Results Info -->
            <div class="results-info" v-if="searchQuery">
                <p>
                    <strong>{{ filteredProducts.length }}</strong> results for 
                    "<strong>{{ searchQuery }}</strong>"
                </p>
            </div>

            <!-- Results Grid -->
            <div class="results-grid" v-if="filteredProducts.length">
                <div v-for="product in filteredProducts" :key="product.id" class="result-card">
                    <NuxtLink :to="`/product/${product.id}`" class="result-link">
                        <div class="result-image">
                            <img :src="product.image_url" :alt="product.name">
                        </div>
                        <div class="result-body">
                            <span class="result-brand" v-if="product.brand">{{ product.brand.name }}</span>
                            <h3>{{ product.name }}</h3>
                            <p class="result-description">{{ product.description?.slice(0, 100) }}...</p>
                            <div class="result-footer">
                                <span class="result-price">${{ product.price.toLocaleString() }}</span>
                                <span class="result-rating" v-if="product.rating">⭐ {{ product.rating }}</span>
                            </div>
                        </div>
                    </NuxtLink>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else class="empty-results">
                <span class="empty-icon">🔍</span>
                <h2>No products found</h2>
                <p v-if="searchQuery">Try different keywords or browse our catalog</p>
                <p v-else>Enter a search term to find products</p>
                <NuxtLink to="/catalog" class="btn btn-outline">Browse Catalog</NuxtLink>
            </div>
        </div>
    </div>
</template>

<style scoped>
.search-page {
    min-height: 80vh;
    padding: 3rem 0;
}

.search-header {
    text-align: center;
    margin-bottom: 3rem;
}

.search-header h1 {
    margin-bottom: 2rem;
}

.search-form {
    display: flex;
    max-width: 600px;
    margin: 0 auto;
    gap: 1rem;
}

.search-input {
    flex: 1;
    margin-bottom: 0;
}

.results-info {
    margin-bottom: 2rem;
    color: var(--text-muted);
}

.results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

.result-card {
    background: white;
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1px solid var(--border);
    transition: all 0.2s;
}

.result-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.result-link {
    display: flex;
    text-decoration: none;
    color: var(--text);
}

.result-image {
    width: 150px;
    flex-shrink: 0;
    padding: 1rem;
    background: #f8fafc;
}

.result-image img {
    width: 100%;
    height: 100px;
    object-fit: contain;
}

.result-body {
    padding: 1.25rem;
    flex: 1;
}

.result-brand {
    font-size: 0.7rem;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 700;
}

.result-body h3 {
    font-size: 1rem;
    margin: 0.5rem 0;
    line-height: 1.3;
}

.result-description {
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
    line-height: 1.4;
}

.result-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.result-price {
    font-size: 1.1rem;
    font-weight: 700;
}

.result-rating {
    font-size: 0.875rem;
    color: #fbbf24;
}

.empty-results {
    text-align: center;
    padding: 4rem 2rem;
}

.empty-icon {
    font-size: 4rem;
    display: block;
    margin-bottom: 1.5rem;
}

.empty-results p {
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}
</style>
