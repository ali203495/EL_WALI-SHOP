<script setup lang="ts">
import { gsap } from 'gsap'

const route = useRoute()
const { translateLanguage } = useLanguage()

// Get initial query from URL
const searchQuery = ref((route.query.q as string) || '')

useHead({
    title: computed(() => searchQuery.value 
        ? `${translateLanguage('search.title')}: ${searchQuery.value}` 
        : translateLanguage('search.title')),
    meta: [
        { name: 'robots', content: 'noindex, follow' }
    ]
})

const api = useApi()
const { data: products, pending: searchLoading, error: searchError, refresh } = await api.getProducts()

const handleRetry = () => {
    refresh()
}

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
        <!-- Loading State -->
        <PageLoading v-if="searchLoading" :message="translateLanguage('catalog.loading')" />

        <!-- Error State -->
        <ErrorState 
            v-else-if="searchError" 
            icon="🔍" 
            :title="translateLanguage('admin.failed_load')" 
            :description="translateLanguage('common.error_desc')"
            :retryable="true"
            @retry="handleRetry"
        >
            <template #footer>
                <div class="error-details">
                    {{ searchError.message || searchError.statusText || searchError }}
                </div>
            </template>
        </ErrorState>

        <div v-else class="container">
            <!-- Brand Blobs -->
            <div class="blob blob-1"></div>
            <div class="blob blob-2"></div>

            <!-- Search Header -->
            <div class="search-header">
                <span class="eyebrow">{{ translateLanguage('catalog.title') }}</span>
                <h1>{{ translateLanguage('search.title') }}</h1>
                <form class="search-form" @submit.prevent="handleSearch">
                    <input 
                        v-model="searchQuery" 
                        type="text" 
                        :placeholder="translateLanguage('search.placeholder')"
                        class="input-field search-input"
                    >
                    <button type="submit" class="btn btn-primary">{{ translateLanguage('common.search_btn') }}</button>
                </form>
            </div>

            <!-- Results Info -->
            <div v-if="searchQuery" class="results-info">
                <p>
                    <strong>{{ filteredProducts.length }}</strong> {{ translateLanguage('search.results_for') }} 
                    "<strong>{{ searchQuery }}</strong>"
                </p>
            </div>

            <!-- Results Grid -->
            <div v-if="filteredProducts.length" class="results-grid">
                <div v-for="product in filteredProducts" :key="product.id" class="result-card">
                    <NuxtLink :to="product?.id ? `/product/${product.id}` : '#'" class="result-link">
                        <div class="result-image">
                            <img :src="product.image_url" :alt="product.name">
                        </div>
                        <div class="result-body">
                            <span v-if="product.brand" class="result-brand">{{ product.brand.name }}</span>
                            <h3>{{ product.name }}</h3>
                            <p class="result-description">{{ product.description?.slice(0, 100) }}...</p>
                            <div class="result-footer">
                                <span v-if="product.price" class="result-price">{{ product.price.toLocaleString() }} {{ translateLanguage('common.currency') }}</span>
                                <span v-if="product.rating" class="result-rating">⭐ {{ product.rating }}</span>
                            </div>
                        </div>
                    </NuxtLink>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else class="empty-results">
                <span class="empty-icon">🔍</span>
                <h2>{{ translateLanguage('search.no_found') }}</h2>
                <p v-if="searchQuery">{{ translateLanguage('search.no_found_q') }}</p>
                <p v-else>{{ translateLanguage('search.no_found_no_q') }}</p>
                <NuxtLink to="/catalog" class="btn btn-outline">{{ translateLanguage('search.browse') }}</NuxtLink>
            </div>
        </div>
    </div>
</template>

<style scoped>
.search-page {
    min-height: 80vh;
    padding: 5rem 0;
    position: relative;
    overflow: hidden;
}

.blob {
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(16, 185, 129, 0.05) 0%, transparent 70%);
    filter: blur(80px);
    z-index: -1;
    pointer-events: none;
}

.blob-1 { top: -100px; right: -200px; }
.blob-2 { bottom: -100px; left: -200px; }

.eyebrow {
    display: block;
    font-size: 0.875rem;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 1rem;
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
    padding: 1.5rem;
    background: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: center;
}

.result-image img {
    width: 100%;
    height: 100px;
    object-fit: contain;
    transition: transform 0.3s ease;
}

.result-card:hover .result-image img {
    transform: scale(1.1);
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
