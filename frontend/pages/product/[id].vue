<script setup lang="ts">
import { gsap } from 'gsap'

const route = useRoute()
const api = useApi()
const { addToCart } = useCart()
const auth = useAuthStore()
const { translateLanguage } = useLanguage()
const { success } = useToast()

const isAdmin = computed(() => auth.user?.is_admin || auth.user?.is_super_admin)

// Fetch product and all products for related
const res = await Promise.all([
    api.getProduct(Number(route.params.id)),
    api.getProducts()
])

const { data: currentProduct, pending: productLoading, error: productError } = res[0]
const { data: allProducts } = res[1]

const globalError = computed(() => productError.value)


const selectedImage = ref('')
const quantity = ref(1)

const incrementQty = () => {
    if (currentProduct.value && quantity.value < (currentProduct.value.stock || 0)) {
        quantity.value++
    }
}

const decrementQty = () => {
    if (quantity.value > 1) {
        quantity.value--
    }
}

// Initialize selected image
watchEffect(() => {
    if (currentProduct.value && currentProduct.value.image_url) {
        selectedImage.value = currentProduct.value.image_url
    }
})

// Related products from same category
const relatedProducts = computed(() => {
    if (!allProducts.value || !currentProduct.value) return []
    return allProducts.value
        .filter((p: any) => p.category_id === currentProduct.value?.category_id && p.id !== currentProduct.value?.id)
        .slice(0, 4)
})

const selectImage = (url: string) => {
    selectedImage.value = url
    gsap.fromTo('.main-image img', { opacity: 0.5 }, { opacity: 1, duration: 0.3 })
}

const handleAddToCart = () => {
    if (!currentProduct.value) return
    
    // Type assertion or default for optional fields
    const productToAdd = {
        ...currentProduct.value,
        image_url: currentProduct.value.image_url || '',
        stock: currentProduct.value.stock || 0
    }
    
    addToCart(productToAdd, quantity.value)
    success(`${currentProduct.value.name} ${translateLanguage('pdp.added_to_cart')}`)
}

// Generate star rating
const starRating = computed(() => {
    const rating = currentProduct.value?.rating || 0
    const full = Math.floor(rating)
    const half = rating % 1 >= 0.5 ? 1 : 0
    return { full, half, empty: 5 - full - half }
})

const handleRetry = () => {
    window.location.reload()
}

// SEO
useHead({
    title: computed(() => currentProduct.value ? `${currentProduct.value.name} | Maison El Wali` : translateLanguage('pdp.details')),
    meta: [
        { name: 'description', content: computed(() => currentProduct.value?.description || translateLanguage('pdp.details')) },
        { property: 'og:title', content: computed(() => currentProduct.value?.name) },
        { property: 'og:description', content: computed(() => currentProduct.value?.description) },
        { property: 'og:image', content: computed(() => currentProduct.value?.image_url) },
        { name: 'twitter:card', content: 'summary_large_image' },
    ]
})

onMounted(() => {
    if (!productLoading.value && !productError.value && currentProduct.value) {
        gsap.from('.product-gallery', { x: -50, opacity: 0, duration: 0.6, ease: 'power2.out' })
        gsap.from('.product-details', { x: 50, opacity: 0, duration: 0.6, ease: 'power2.out', delay: 0.1 })
        gsap.from('.related-card', { y: 30, opacity: 0, stagger: 0.1, duration: 0.5, delay: 0.3 })
    }
})
</script>

<template>
    <div class="pdp-wrapper">
        <!-- Loading State -->
        <PageLoading v-if="productLoading" :message="translateLanguage('pdp.loading')" />
        
        <!-- Error State -->
        <ErrorState 
            v-else-if="globalError || !currentProduct"
            icon="⚠️"
            :title="translateLanguage('pdp.not_found')"
            :description="translateLanguage('pdp.not_found_desc')"
            :retryable="true"
            @retry="handleRetry"
        >
            <template v-if="globalError" #footer>
                <div class="error-details">
                    {{ globalError.message || globalError.statusText || globalError }}
                </div>
            </template>
        </ErrorState>

        <!-- Content -->
        <div v-else class="pdp-page">
            <div class="container">
                <!-- Breadcrumbs -->
                <nav class="breadcrumbs">
                    <NuxtLink to="/">{{ translateLanguage('pdp.home') }}</NuxtLink>
                    <span class="separator">/</span>
                    <NuxtLink to="/catalog">{{ translateLanguage('pdp.catalog') }}</NuxtLink>
                    <span class="separator">/</span>
                    <span class="current">{{ currentProduct.name }}</span>
                </nav>

                <div class="product-main">
                    <!-- Gallery -->
                    <div class="product-gallery">
                        <div class="main-image">
                            <img :src="selectedImage" :alt="currentProduct.name">
                        </div>
                        <div class="thumbnails">
                            <button 
                                v-for="(img, index) in [currentProduct.image_url, ...(currentProduct.additional_images || [])]" 
                                :key="index"
                                class="thumb-btn"
                                :class="{ active: selectedImage === img }"
                                @click="img && selectImage(img)"
                            >
                                <img :src="img" :alt="`${currentProduct.name} view ${index + 1}`">
                            </button>
                        </div>
                    </div>

                    <!-- Details -->
                    <div class="product-details">
                        <div class="product-header">
                            <span v-if="currentProduct.brand" class="brand">{{ currentProduct.brand.name }}</span>
                            <div class="header-main">
                                <h1>{{ currentProduct.name }}</h1>
                                <NuxtLink 
                                    v-if="isAdmin" 
                                    :to="`/admin/products?id=${currentProduct.id}`" 
                                    class="btn btn-sm btn-outline edit-btn"
                                >
                                    ✏️ {{ translateLanguage('admin.edit') || 'Edit' }}
                                </NuxtLink>
                            </div>
                            <div class="rating-review">
                                <div class="stars">
                                    <span v-for="n in starRating.full" :key="`full-${n}`">⭐</span>
                                    <span v-if="starRating.half">⭐️</span> 
                                </div>
                                <span class="review-count">({{ currentProduct.review_count || 0 }} {{ translateLanguage('pdp.reviews') }})</span>
                            </div>
                        </div>

                        <div class="price-section">
                            <span class="price">{{ currentProduct.price.toLocaleString() }} {{ translateLanguage('common.currency') }}</span>
                            <span class="stock-status" :class="{ 'in-stock': currentProduct.stock > 0, 'out-stock': currentProduct.stock === 0 }">
                                {{ currentProduct.stock > 0 ? translateLanguage('pdp.in_stock') : translateLanguage('pdp.out_stock') }}
                            </span>
                        </div>

                        <p class="description">{{ currentProduct.description }}</p>

                        <div v-if="currentProduct.stock > 0" class="actions-wrapper">
                            <div class="qty-selector-pdp">
                                <label>{{ translateLanguage('pdp.quantity') }}</label>
                                <div class="qty-controls">
                                    <button class="qty-btn" :disabled="quantity <= 1" @click="decrementQty">−</button>
                                    <span class="qty-value">{{ quantity }}</span>
                                    <button class="qty-btn" :disabled="quantity >= currentProduct.stock" @click="incrementQty">+</button>
                                </div>
                            </div>
                            <div class="actions">
                                <button 
                                    class="btn btn-lg btn-primary add-cart-btn"
                                    @click="handleAddToCart"
                                >
                                    {{ translateLanguage('pdp.add_to_cart') }}
                                </button>
                                <button class="btn btn-lg btn-outline wishlist-btn">
                                    ❤️
                                </button>
                            </div>
                        </div>
                        <div v-else class="actions">
                            <button class="btn btn-lg btn-primary add-cart-btn" disabled>
                                {{ translateLanguage('pdp.out_stock') }}
                            </button>
                        </div>

                        <!-- Specs -->
                        <div v-if="currentProduct.specs" class="specs-section">
                            <h3>{{ translateLanguage('pdp.specs') }}</h3>
                            <dl class="specs-grid">
                                <template v-for="(value, key) in currentProduct.specs" :key="key">
                                    <dt>{{ String(key).replace(/_/g, ' ') }}</dt>
                                    <dd>{{ value }}</dd>
                                </template>
                            </dl>
                        </div>
                    </div>
                </div>

                <!-- Related Products -->
                <section v-if="relatedProducts.length > 0" class="related-products">
                    <h2>{{ translateLanguage('pdp.related') }}</h2>
                    <div class="related-grid">
                        <NuxtLink 
                            v-for="product in relatedProducts" 
                            :key="product.id"
                            :to="`/product/${product.id}`"
                            class="related-card"
                        >
                            <div class="related-image">
                                <img :src="product.image_url" :alt="product.name">
                            </div>
                            <div class="related-info">
                                <h4>{{ product.name }}</h4>
                                <span class="related-price">{{ product.price.toLocaleString() }} {{ translateLanguage('common.currency') }}</span>
                            </div>
                        </NuxtLink>
                    </div>
                </section>
                
                <!-- CTA -->
                 <section class="store-cta-section">
                    <div class="cta-content">
                        <h2>{{ translateLanguage('stores.experience_person') }}</h2>
                        <p>{{ translateLanguage('stores.experience_desc') }}</p>
                        <NuxtLink to="/stores" class="btn btn-primary">{{ translateLanguage('about.find_store') }}</NuxtLink>
                    </div>
                </section>
            </div>
        </div>
    </div>
</template>

<style scoped>
.pdp-wrapper {
    min-height: 80vh;
}

.pdp-page {
    padding-bottom: 4rem;
}

.breadcrumbs {
    padding: 1.5rem 0;
    color: var(--text-muted);
    font-size: 0.875rem;
    display: flex;
    gap: 0.5rem;
}

.breadcrumbs a {
    color: var(--text-muted);
    text-decoration: none;
}

.breadcrumbs a:hover {
    color: var(--primary);
}

.separator {
    color: var(--text-muted);
    opacity: 0.5;
}

.current {
    color: var(--text);
    font-weight: 600;
}

.product-main {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 4rem;
    margin-bottom: 4rem;
}

/* Gallery */
.product-gallery {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.main-image {
    background: white;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    padding: 2rem;
    height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.main-image img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.thumbnails {
    display: flex;
    gap: 1rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
}

.thumb-btn {
    width: 80px;
    height: 80px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.5rem;
    background: white;
    cursor: pointer;
    transition: all 0.2s;
}

.thumb-btn.active {
    border-color: var(--primary);
    box-shadow: 0 0 0 2px var(--primary-light);
}

.thumb-btn img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

/* Details */
.product-header {
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}

.brand {
    color: var(--primary);
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.875rem;
    letter-spacing: 0.1em;
    display: block;
    margin-bottom: 0.5rem;
}

h1 {
    font-size: 2.5rem;
    line-height: 1.1;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--text) 0%, var(--text-muted) 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.header-main {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1.5rem;
}

.edit-btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.875rem;
    border-color: var(--primary);
    color: var(--primary);
    white-space: nowrap;
}

.rating-review {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-muted);
}

.stars {
    color: #fbbf24;
}

.price-section {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.price {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
}

.stock-status {
    font-size: 0.875rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
}

.in-stock {
    background: #dcfce7;
    color: #16a34a;
}

.out-stock {
    background: #fee2e2;
    color: #dc2626;
}

.description {
    color: var(--text-muted);
    font-size: 1.125rem;
    line-height: 1.7;
    margin-bottom: 2rem;
}

/* Actions */
.actions-wrapper {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 3rem;
}

.qty-selector-pdp {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    background: var(--surface);
    padding: 1rem;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    width: fit-content;
}

.qty-selector-pdp label {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.qty-controls {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.qty-btn {
    width: 40px;
    height: 40px;
    border: none;
    background: white;
    border-radius: var(--radius-sm);
    font-size: 1.25rem;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-sm);
}

.qty-btn:hover:not(:disabled) {
    background: var(--primary);
    color: white;
}

.qty-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.qty-value {
    font-size: 1.25rem;
    font-weight: 700;
    min-width: 40px;
    text-align: center;
}

.actions {
    display: flex;
    gap: 1rem;
}

.add-cart-btn {
    flex: 1;
}

.specs-section h3 {
    font-size: 1.25rem;
    margin-bottom: 1rem;
}

.specs-grid {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 1rem 2rem;
}

.specs-grid dt {
    font-weight: 600;
    color: var(--text);
    text-transform: capitalize;
}

.specs-grid dd {
    color: var(--text-muted);
}

/* Related */
.related-products {
    margin-top: 4rem;
}

.related-products h2 {
    margin-bottom: 2rem;
}

.related-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 2rem;
}

.related-card {
    display: block;
    text-decoration: none;
    color: var(--text);
    background: white;
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid var(--border);
    transition: all 0.3s;
}

.related-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.related-image {
    height: 180px;
    padding: 1rem;
    background: #f8fafc;
}

.related-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.related-info {
    padding: 1rem;
}

.related-info h4 {
    font-size: 0.9rem;
    margin: 0.25rem 0 0.75rem;
}

.related-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.related-price {
    font-weight: 700;
}
</style>
