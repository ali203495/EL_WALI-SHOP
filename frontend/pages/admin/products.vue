<script setup lang="ts">
import { ref, computed } from 'vue'
import gsap from 'gsap'

const api = useApi()
const { success, error: showError } = useToast()
const loading = ref(false)

definePageMeta({
    layout: 'admin'
})

// Fetch Data
const [
    { data: products, refresh },
    { data: categories },
    { data: brands }
] = await Promise.all([
    api.getProducts(),
    api.getCategories(),
    api.getBrands()
])

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
            success('تم تحديث المنتج بنجاح')

        } else {
            // Create mode - Real
            await api.createProduct(formData)
            success('تم إنشاء المنتج بنجاح')
        }
        showAddModal.value = false
        showEditModal.value = false
        await refresh()
    } catch (e) {
        console.error(e)
        showError('فشل حفظ المنتج')
    } finally {
        loading.value = false
    }
}

const handleDeleteProduct = async () => {
    if (!selectedProduct.value?.id) return
    
    try {
        await api.deleteProduct(selectedProduct.value.id)
        success('تم حذف المنتج بنجاح')
    } catch (e: any) {
        // Show specific error from backend if available
        const msg = e.data?.detail || 'فشل حذف المنتج'
        showError(msg)
    }
    
    showDeleteDialog.value = false
    selectedProduct.value = null
    await refresh()
}


onMounted(() => {
    gsap.from('.product-row', {
        x: -20,
        opacity: 0,
        stagger: 0.03,
        duration: 0.4
    })
})
</script>

<template>
    <div dir="rtl">
        <!-- Main Content -->
        <main class="content">
            <header class="page-header">
                <div>
                    <h1>المنتجات</h1>
                    <p class="subtitle">إدارة كتالوج المنتجات</p>
                </div>
                <button class="btn btn-primary" @click="openAddModal">+ إضافة منتج</button>
            </header>

            <!-- Search & Filter -->
            <div class="toolbar">
                <input 
                    v-model="searchQuery" 
                    type="text" 
                    placeholder="بحث عن المنتجات..." 
                    class="input-field search-input"
                >
                <span class="count">{{ filteredProducts.length }} منتج</span>
            </div>

            <!-- Products Table -->
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>المنتج</th>
                            <th>الماركة</th>
                            <th>الفئة</th>
                            <th>السعر</th>
                            <th>المخزون</th>
                            <th>التقييم</th>
                            <th>إجراءات</th>
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
                            <td class="price">${{ product.price.toLocaleString() }}</td>
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
                                    <button class="action-btn edit" title="Edit" @click="openEditModal(product)">✏️</button>
                                    <button class="action-btn delete" title="Delete" @click="openDeleteDialog(product)">🗑️</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </main>

        <!-- Add Product Modal -->
        <Modal v-model="showAddModal" title="إضافة منتج جديد" size="lg">
            <ProductForm 
                :categories="categories || []" 
                :brands="brands || []"
                @submit="handleSubmitProduct"
                @cancel="showAddModal = false"
            />
        </Modal>

        <!-- Edit Product Modal -->
        <Modal v-model="showEditModal" title="تعديل المنتج" size="lg">
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
            title="حذف المنتج"
            :message="`هل أنت متأكد من حذف '${selectedProduct?.name}'؟ لا يمكن التراجع عن هذا الإجراء.`"
            confirmText="حذف"
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

.search-input {
    width: 300px;
    margin-bottom: 0;
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
</style>
