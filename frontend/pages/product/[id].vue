```vue
<script setup lang="ts">
import gsap from 'gsap'

const route = useRoute()
const api = useApi()
const { addToCart } = useCart()
const { success } = useToast()

// Fetch product and all products for related
const [
    { data: currentProduct, pending: productLoading, error: productError },
    { data: allProducts }
] = await Promise.all([
    api.getProduct(Number(route.params.id)),
    api.getProducts()
])

const quantity = ref(1)
const selectedImage = ref('')

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
        .filter(p => p.category_id === currentProduct.value?.category_id && p.id !== currentProduct.value?.id)
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
    
    addToCart(productToAdd)
    // Update quantity if needed (though useCart handles simple add)
    // In a real app we might pass quantity to addToCart
    
    success(`${currentProduct.value.name} has been added to your cart.`)
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
    title: computed(() => currentProduct.value ? currentProduct.value.name : 'Product Details'),
    meta: [
        { name: 'description', content: computed(() => currentProduct.value?.description || 'Product details') },
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
        <PageLoading v-if="productLoading" message="Loading product details..." />
        
        <!-- Error State -->
        <ErrorState 
            v-else-if="productError || !currentProduct"
            icon="⚠️"
            title="Product Not Found"
            description="The product you are looking for does not exist or could not be loaded."
            :retryable="true"
            @retry="handleRetry"
        />

        <!-- Content -->
        <div v-else class="pdp-page">
            <div class="container">
                <!-- Breadcrumbs -->
                <nav class="breadcrumbs">
                    <NuxtLink to="/">Home</NuxtLink>
                    <span class="separator">/</span>
                    <NuxtLink to="/catalog">Catalog</NuxtLink>
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
                                @click="selectImage(img)"
                            >
                                <img :src="img" :alt="`${currentProduct.name} view ${index + 1}`">
                            </button>
                        </div>
                    </div>

                    <!-- Details -->
                    <div class="product-details">
                        <div class="product-header">
                            <span class="brand" v-if="currentProduct.brand">{{ currentProduct.brand.name }}</span>
                            <h1>{{ currentProduct.name }}</h1>
                            <div class="rating-review">
                                <div class="stars">
                                    <span v-for="n in starRating.full" :key="`full-${n}`">⭐</span>
                                    <span v-if="starRating.half">⭐️</span> 
                                </div>
                                <span class="review-count">({{ currentProduct.review_count || 0 }} reviews)</span>
                            </div>
                        </div>

                        <div class="price-section">
                            <span class="price">${{ currentProduct.price.toLocaleString() }}</span>
                            <span class="stock-status" :class="{ 'in-stock': currentProduct.stock > 0, 'out-stock': currentProduct.stock === 0 }">
                                {{ currentProduct.stock > 0 ? 'In Stock' : 'Out of Stock' }}
                            </span>
                        </div>

                        <p class="description">{{ currentProduct.description }}</p>

                        <div class="actions">
                            <button 
                                class="btn btn-lg btn-primary add-cart-btn"
                                :disabled="currentProduct.stock === 0"
                                @click="handleAddToCart"
                            >
                                {{ currentProduct.stock > 0 ? 'Add to Cart' : 'Out of Stock' }}
                            </button>
                            <button class="btn btn-lg btn-outline wishlist-btn">
                                ❤️
                            </button>
                        </div>

                        <!-- Specs -->
                        <div class="specs-section" v-if="currentProduct.specs">
                            <h3>Specifications</h3>
                            <dl class="specs-grid">
                                <template v-for="(value, key) in currentProduct.specs" :key="key">
                                    <dt>{{ key.replace(/_/g, ' ') }}</dt>
                                    <dd>{{ value }}</dd>
                                </template>
                            </dl>
                        </div>
                    </div>
                </div>

                <!-- Related Products -->
                <section class="related-products" v-if="relatedProducts.length > 0">
                    <h2>You Might Also Like</h2>
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
                                <span class="related-price">${{ product.price.toLocaleString() }}</span>
                            </div>
                        </NuxtLink>
                    </div>
                </section>
                
                <!-- CTA -->
                 <section class="store-cta-section">
                    <div class="cta-content">
                        <h2>Experience it in Person</h2>
                        <p>Visit one of our premium showrooms to test this product before you buy.</p>
                        <NuxtLink to="/stores" class="btn btn-primary">Find a Store</NuxtLink>
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
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
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

.actions {
    display: flex;
    gap: 1rem;
    margin-bottom: 3rem;
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
