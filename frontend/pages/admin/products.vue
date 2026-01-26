<script setup lang="ts">
import { ref, computed } from 'vue'
import { gsap } from 'gsap'
const { translateLanguage } = useLanguage()
const route = useRoute()
const router = useRouter()

const api = useApi()
const { success, error: showError } = useToast()

definePageMeta({
    layout: 'admin'
})

// Fetch products
const products = ref<any[]>([])
const categories = ref<any[]>([])
const brands = ref<any[]>([])
const loading = ref(true)
const error = ref<any>(null)

const fetchData = async () => {
    loading.value = true
    error.value = null
    try {
        const [p, c, b] = await Promise.all([
            api.getProducts(),
            api.getCategories(),
            api.getBrands()
        ])
        
        if (p.error.value || c.error.value || b.error.value) {
            error.value = p.error.value || c.error.value || b.error.value
            return
        }

        products.value = p.data.value || []
        categories.value = c.data.value || []
        brands.value = b.data.value || []
    } catch (e) {
        error.value = e
        console.error('Fetch products failed:', e)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchData()
    gsap.from('.product-row', {
        x: -20,
        opacity: 0,
        stagger: 0.03,
        duration: 0.4
    })
})

const searchQuery = ref('')
const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteDialog = ref(false)
const selectedProduct = ref<any>(null)

const filteredProducts = computed(() => {
    if (!products.value) return []
    if (!searchQuery.value) return products.value
    const q = searchQuery.value.toLowerCase()
    return products.value.filter(p => 
        p.name.toLowerCase().includes(q) ||
        p.brand?.name.toLowerCase().includes(q)
    )
})

const openAddModal = () => {
    selectedProduct.value = null
    showAddModal.value = true
}

const openEditModal = (product: any) => {
    selectedProduct.value = { ...product }
    showEditModal.value = true
}

const openDeleteDialog = (product: any) => {
    selectedProduct.value = product
    showDeleteDialog.value = true
}

const handleSubmitProduct = async (formData: any) => {
    loading.value = true
    try {
        if (selectedProduct.value?.id) {
            // Edit mode - Real
            await api.updateProduct(selectedProduct.value.id, formData)
            success(translateLanguage('admin.save_success'))

        } else {
            // Create mode - Real
            await api.createProduct(formData)
            success(translateLanguage('admin.save_success'))
        }
        showAddModal.value = false
        showEditModal.value = false
        await fetchData()
    } catch (e: any) {
        console.error(e)
        showError(translateLanguage('admin.save_failed'))
    } finally {
        loading.value = false
    }
}

const handleDeleteProduct = async () => {
    if (!selectedProduct.value?.id) return
    
    try {
        await api.deleteProduct(selectedProduct.value.id)
        success(translateLanguage('admin.delete_success'))
    } catch (e: any) {
        // Show specific error from backend if available
        const msg = e.data?.detail || translateLanguage('admin.failed_load')
        showError(msg)
    }
    
    showDeleteDialog.value = false
    selectedProduct.value = null
    await fetchData()
}

// Handle direct edit via ID
watch([products, () => route.query.id], () => {
    if (route.query.id && products.value.length > 0) {
        const product = products.value.find(p => p.id === Number(route.query.id))
        if (product) {
            openEditModal(product)
            router.replace({ query: { ...route.query, id: undefined } })
        }
    }
}, { immediate: true })
</script>

<template>
    <div>
        <!-- Main Content -->
        <main class="content">
            <header class="page-header">
                <div>
                    <h1>{{ translateLanguage('admin.products') }}</h1>
                    <p class="subtitle">{{ translateLanguage('nav.admin_portal') }} / {{ translateLanguage('admin.products') }}</p>
                </div>
                <button class="btn btn-primary" @click="openAddModal">+ {{ translateLanguage('admin.add_product') }}</button>
            </header>

            <!-- Search & Filter -->
            <div class="toolbar">
                <div class="search-wrapper">
                    <span class="search-icon">🔍</span>
                    <input 
                        v-model="searchQuery" 
                        type="text" 
                        :placeholder="translateLanguage('admin.search_placeholder')" 
                        class="input-field search-input"
                    >
                </div>
                <span class="count">{{ filteredProducts.length }} {{ translateLanguage('admin.product') }}</span>
            </div>

            <!-- Products Table -->
            <div class="table-container">
                <div v-if="loading" class="loading-state">
                    <Spinner size="lg" color="var(--primary)" />
                    <p>{{ translateLanguage('admin.loading_data') }}</p>
                </div>
                <div v-else-if="filteredProducts.length === 0" class="empty-state">
                    <div class="empty-icon">📦</div>
                    <h3>{{ translateLanguage('admin.no_products') }}</h3>
                    <p>{{ translateLanguage('admin.no_products') }}</p>
                    <button class="btn btn-primary" @click="openAddModal">{{ translateLanguage('admin.add_product') }}</button>
                </div>
                <table v-else class="data-table">
                    <thead>
                        <tr>
                            <th>{{ translateLanguage('admin.product') }}</th>
                            <th>{{ translateLanguage('admin.brand') }}</th>
                            <th>{{ translateLanguage('admin.category') }}</th>
                            <th>{{ translateLanguage('admin.price') }}</th>
                            <th>{{ translateLanguage('admin.stock') }}</th>
                            <th>{{ translateLanguage('admin.rating') }}</th>
                            <th>{{ translateLanguage('admin.actions') }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="product in filteredProducts" :key="product.id" class="product-row">
                            <td>
                                <div class="product-cell">
                                    <img :src="product.image_url" :alt="product.name" class="product-thumb">
                                    <div>
                                        <span class="product-name">{{ product.name }}</span>
                                        <span class="product-id">#{{ product.id }}</span>
                                    </div>
                                </div>
                            </td>
                            <td>{{ product.brand?.name || '-' }}</td>
                            <td>{{ product.category?.name || '-' }}</td>
                            <td class="price">{{ translateLanguage('common.currency') }} {{ product.price.toLocaleString() }}</td>
                            <td>
                                <span class="stock-badge" :class="{ 'low': product.stock < 30 }">
                                    {{ product.stock }}
                                </span>
                            </td>
                            <td>
                                <span class="rating">⭐ {{ product.rating || '-' }}</span>
                            </td>
                            <td>
                                <div class="actions">
                                    <button class="action-btn edit" :title="translateLanguage('admin.edit')" @click="openEditModal(product)">✏️</button>
                                    <button class="action-btn delete" :title="translateLanguage('admin.delete')" @click="openDeleteDialog(product)">🗑️</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </main>

        <!-- Add Product Modal -->
        <Modal v-model="showAddModal" :title="translateLanguage('admin.add_product')" size="lg">
            <ProductForm 
                :categories="categories || []" 
                :brands="brands || []"
                @submit="handleSubmitProduct"
                @cancel="showAddModal = false"
            />
        </Modal>

        <!-- Edit Product Modal -->
        <Modal v-model="showEditModal" :title="translateLanguage('admin.edit')" size="lg">
            <ProductForm 
                :product="selectedProduct"
                :categories="categories || []" 
                :brands="brands || []"
                @submit="handleSubmitProduct"
                @cancel="showEditModal = false"
            />
        </Modal>

        <!-- Delete Confirmation Dialog -->
        <ConfirmDialog
            v-model="showDeleteDialog"
            :title="translateLanguage('admin.delete')"
            :message="translateLanguage('admin.delete_confirm').replace('{name}', selectedProduct?.name)"
            :confirm-text="translateLanguage('admin.delete')"
            variant="danger"
            @confirm="handleDeleteProduct"
            @cancel="showDeleteDialog = false"
        />
    </div>
</template>

<style scoped>
/* Page specific styles */
.content {
    padding: 2rem 3rem;
    overflow-y: auto;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.subtitle {
    color: #4b5563; /* Darker grey for better readability */
    margin-top: 0.25rem;
    font-weight: 500;
}

.toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.search-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.search-icon {
    position: absolute;
    left: 1rem;
    color: #94a3b8;
    pointer-events: none;
}

.search-input {
    width: 320px;
    margin-bottom: 0;
    padding-left: 2.75rem !important;
    background: white;
}

.count {
    color: var(--text-muted);
    font-size: 0.875rem;
}

.table-container {
    background: var(--surface);
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.data-table th,
.data-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

.data-table th {
    background: #f8fafc;
    font-weight: 700;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
    border-bottom: 2px solid #e2e8f0;
}

.product-row {
    transition: all 0.2s;
}

.product-row:hover {
    background: #fcfdfd;
    transform: scale(1.002);
}

/* Global table styles used */
.product-cell {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.product-thumb {
    width: 48px;
    height: 48px;
    object-fit: cover;
    border-radius: 0.5rem;
    background: #f8fafc;
}

.product-name {
    display: block;
    font-weight: 600;
}

.product-id {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.price {
    font-weight: 600;
}

.stock-badge {
    /* Using component specific override for stock warning */
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}

.stock-badge {
     background: rgba(16, 185, 129, 0.1);
     color: var(--success);
}

.stock-badge.low {
    background: rgba(245, 158, 11, 0.1);
    color: var(--accent-warm);
}

.rating {
    color: #fbbf24;
}

.actions {
    display: flex;
    gap: 0.5rem;
}

.action-btn {
    background: none;
    border: none;
    font-size: 1rem;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 0.25rem;
    transition: background 0.2s;
}

.action-btn:hover {
    background: #f1f5f9;
}

.action-btn.delete:hover {
    background: #fef2f2;
}

.loading-state, .empty-state {
    padding: 5rem 2rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

.empty-state h3 {
    margin-bottom: 0.5rem;
    color: var(--text);
}

.empty-state p {
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}
</style>
