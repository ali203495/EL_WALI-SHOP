<script setup lang="ts">
import { gsap } from 'gsap'

const api = useApi()

// Fetch all data with loading and error handling
const res = await Promise.all([
    api.getProducts(),
    api.getCategories(),
    api.getBrands()
])

const { data: products, pending: productsLoading, error: productsError, refresh: refreshProducts } = res[0]
const { data: categories, error: categoriesError } = res[1]
const { data: brands, error: brandsError } = res[2]

const globalError = computed(() => productsError.value || categoriesError.value || brandsError.value)

// Filters
const searchQuery = ref('')
const selectedCategory = ref<number | null>(null)
const selectedBrand = ref<number | null>(null)
const sortBy = ref('featured')

const filteredProducts = computed(() => {
    if (!products.value) return []
    
    let result = [...products.value]
    
    // Text search
    if (searchQuery.value) {
        const q = searchQuery.value.toLowerCase()
        result = result.filter(p => 
            p.name.toLowerCase().includes(q) ||
            p.description?.toLowerCase().includes(q) ||
            p.brand?.name?.toLowerCase().includes(q)
        )
    }
    
    // Category filter
    if (selectedCategory.value) {
        result = result.filter(p => p.category_id === selectedCategory.value)
    }
    
    // Brand filter
    if (selectedBrand.value) {
        result = result.filter(p => p.brand_id === selectedBrand.value)
    }
    
    // Sort
    switch (sortBy.value) {
        case 'price-low':
            result.sort((a, b) => a.price - b.price)
            break
        case 'price-high':
            result.sort((a, b) => b.price - a.price)
            break
        case 'rating':
            result.sort((a, b) => (b.rating || 0) - (a.rating || 0))
            break
    }
    
    return result
})

const clearFilters = () => {
    searchQuery.value = ''
    selectedCategory.value = null
    selectedBrand.value = null
    sortBy.value = 'featured'
}

const handleRetry = () => {
    refreshProducts()
}

onMounted(() => {
    if (productsError.value) {
        // console.error('Products Error:', productsError.value)
    }

    if (!productsLoading.value && !productsError.value) {
        gsap.from('.product-card', {
            y: 30,
            opacity: 0,
            stagger: 0.05,
            duration: 0.5,
            ease: 'power2.out'
        })
    }
})

const auth = useAuthStore()
const isAdmin = computed(() => auth.user?.is_admin || auth.user?.is_super_admin)
const { translateLanguage } = useLanguage()

// SEO
useHead({
    title: translateLanguage('catalog.title')
})

const showQuickView = ref(false)
const quickViewProduct = ref(null)

const openQuickView = (product: any) => {
    quickViewProduct.value = product
    showQuickView.value = true
}
</script>

<template>
    <div class="catalog-page">
        <!-- Loading State -->
        <PageLoading v-if="productsLoading" :message="translateLanguage('catalog.loading')" />
        
        <!-- Error State -->
        <ErrorState 
            v-else-if="globalError"
            icon="❌"
            :title="translateLanguage('catalog.failed')"
            :description="translateLanguage('catalog.error_desc')"
            :retryable="true"
            @retry="handleRetry"
        >
            <template #footer>
                <div class="error-details">
                    {{ globalError.message || globalError.statusText || globalError }}
                </div>
            </template>
        </ErrorState>
        
        <!-- Content -->
        <template v-else>
            <!-- Sidebar Filters -->
            <aside class="filter-sidebar">
                <div class="filter-header">
                    <h3>{{ translateLanguage('catalog.filters') }}</h3>
                    <button class="clear-btn" @click="clearFilters">{{ translateLanguage('catalog.clear_all') }}</button>
                </div>
                
                <!-- Categories -->
                <div class="filter-section">
                    <h4>{{ translateLanguage('catalog.categories') }}</h4>
                    <ul class="filter-list">
                        <li 
                            v-for="cat in categories" 
                            :key="cat.id"
                            :class="{ active: selectedCategory === cat.id }"
                            @click="selectedCategory = selectedCategory === cat.id ? null : cat.id"
                        >
                            {{ cat.name }}
                        </li>
                    </ul>
                </div>
                
                <!-- Brands -->
                <div class="filter-section">
                    <h4>{{ translateLanguage('catalog.brands') }}</h4>
                    <ul class="filter-list">
                        <li 
                            v-for="brand in brands" 
                            :key="brand.id"
                            :class="{ active: selectedBrand === brand.id }"
                            @click="selectedBrand = selectedBrand === brand.id ? null : brand.id"
                        >
                            {{ brand.name }}
                        </li>
                    </ul>
                </div>

                <!-- Admin Quick Links -->
                <div v-if="isAdmin" class="filter-section admin-section">
                    <h4>💎 {{ translateLanguage('catalog.quick_actions') }}</h4>
                    <ul class="filter-list">
                        <li>
                            <NuxtLink to="/admin/categories">📂 {{ translateLanguage('catalog.edit_categories') }}</NuxtLink>
                        </li>
                        <li>
                            <NuxtLink to="/admin/brands">🏷️ {{ translateLanguage('catalog.edit_brands') }}</NuxtLink>
                        </li>
                    </ul>
                </div>
            </aside>
            
            <!-- Main Content -->
            <main class="catalog-content">
                <header class="catalog-header">
                    <div class="header-left">
                        <h1>{{ translateLanguage('catalog.title') }}</h1>
                        <span class="product-count">{{ filteredProducts.length }} {{ translateLanguage('catalog.count_plural') }}</span>
                    </div>
                    <div class="header-controls">
                        <input 
                            v-model="searchQuery" 
                            type="text" 
                            :placeholder="translateLanguage('catalog.search_placeholder')" 
                            class="input-field search-input"
                        >
                        <select v-model="sortBy" class="input-field sort-select">
                            <option value="featured">{{ translateLanguage('catalog.sort_featured') }}</option>
                            <option value="price-low">{{ translateLanguage('catalog.sort_price_low') }}</option>
                            <option value="price-high">{{ translateLanguage('catalog.sort_price_high') }}</option>
                            <option value="rating">{{ translateLanguage('catalog.sort_rating') }}</option>
                        </select>
                    </div>
                </header>
                
                <!-- Active Filters -->
                <div v-if="selectedCategory || selectedBrand" class="active-filters">
                    <span v-if="selectedCategory" class="filter-tag" @click="selectedCategory = null">
                        {{ categories?.find(c => c.id === selectedCategory)?.name }} ×
                    </span>
                    <span v-if="selectedBrand" class="filter-tag" @click="selectedBrand = null">
                        {{ brands?.find(b => b.id === selectedBrand)?.name }} ×
                    </span>
                </div>
                
                <!-- Product Grid -->
                <div class="product-grid">
                    <ProductCard 
                        v-for="product in filteredProducts" 
                        :key="product.id" 
                        :product="product"
                        :show-badge="!!product.rating"
                        @quick-view="openQuickView"
                    />
                </div>
                
                <!-- Empty State -->
                <EmptyState 
                    v-if="filteredProducts.length === 0"
                    icon="🔍"
                    :title="translateLanguage('catalog.no_found')"
                    :description="translateLanguage('catalog.no_found_desc')"
                >
                    <template #actions>
                        <button class="btn btn-outline" @click="clearFilters">{{ translateLanguage('catalog.clear_all') }}</button>
                    </template>
                </EmptyState>
            </main>
        </template>

        <ProductQuickView 
            v-if="quickViewProduct" 
            :is-open="showQuickView" 
            :product="quickViewProduct" 
            @close="showQuickView = false"
        />
    </div>
</template>

<style scoped>
.catalog-page {
    display: grid;
    grid-template-columns: 280px 1fr;
    min-height: 100vh;
}

/* Sidebar */
.filter-sidebar {
    background: var(--surface);
    padding: 2rem;
    border-right: 1px solid var(--border);
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
}

.filter-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}

.clear-btn {
    background: none;
    border: none;
    color: var(--primary);
    font-size: 0.875rem;
    cursor: pointer;
}

.filter-section {
    margin-bottom: 2rem;
}

.filter-section h4 {
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 1rem;
}

.filter-list {
    list-style: none;
}

.filter-list li {
    padding: 0.75rem 1rem;
    margin: 0.25rem 0;
    border-radius: var(--radius);
    cursor: pointer;
    transition: all 0.2s;
}

.filter-list li:hover {
    background: var(--primary-light);
}

.filter-list li.active {
    background: var(--primary);
    color: white;
}

.admin-section {
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 2px dashed var(--border);
}

.admin-section h4 {
    color: var(--primary);
}

.admin-section .filter-list li {
    padding: 0;
}

.admin-section .filter-list a {
    display: block;
    padding: 0.75rem 1rem;
    color: inherit;
    text-decoration: none;
}

/* Main Content */
.catalog-content {
    padding: 2rem 3rem;
    background: var(--background);
}

.catalog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.header-left {
    display: flex;
    align-items: baseline;
    gap: 1rem;
}

.product-count {
    color: var(--text-muted);
    font-size: 0.875rem;
}

.header-controls {
    display: flex;
    gap: 1rem;
}

.search-input {
    width: 250px;
    margin-bottom: 0;
}

.sort-select {
    width: 180px;
    margin-bottom: 0;
}

.active-filters {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.filter-tag {
    background: var(--primary-light);
    color: var(--primary);
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    cursor: pointer;
}

/* Product Grid */
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
}

@media (max-width: 1024px) {
    .catalog-page {
        grid-template-columns: 1fr;
    }
    
    .filter-sidebar {
        display: none;
    }
}
</style>
