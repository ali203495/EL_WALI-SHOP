<script setup lang="ts">
import { gsap } from 'gsap'
import AdminSalesChart from '~/components/admin/SalesChart.vue'
const { translateLanguage } = useLanguage()

definePageMeta({
    layout: 'admin'
})

const auth = useAuthStore()
const api = useApi()

// Fetch dashboard stats
const error = ref<any>(null)
const loading = ref(true)

const fetchData = async () => {
    loading.value = true
    error.value = null
    try {
        const [p, b, s, c, o] = await Promise.all([
            api.getProducts(),
            api.getBrands(),
            api.getStores(),
            api.getCategories(),
            api.getOrders()
        ])
        
        // Handle potential errors from useFetch results
        const anyError = p.error.value || b.error.value || s.error.value || c.error.value || o.error.value
        if (anyError) {
            error.value = anyError
            return
        }

        products.value = p.data.value || []
        brands.value = b.data.value || []
        stores.value = s.data.value || []
        categories.value = c.data.value || []
        orders.value = o.data.value || []
    } catch (e: any) {
        console.error('Dashboard fetch error:', e)
        error.value = e
    } finally {
        loading.value = false
    }
}

const products = ref<any[]>([])
const brands = ref<any[]>([])
const stores = ref<any[]>([])
const categories = ref<any[]>([])
const orders = ref<any[]>([])

// Calculate Total Revenue
const totalRevenue = computed(() => {
    return orders.value?.reduce((acc: number, order: any) => acc + (order.total_amount || 0), 0) || 0
})

// Low Stock Items
const lowStockProducts = computed(() => {
    return products.value?.filter(p => p.stock <= 5) || []
})

const stats = computed(() => [
    { label: 'Creations', value: products.value?.length || 0, icon: '✨', color: 'var(--primary)', key: 'nav.products' },
    { label: 'Artisans', value: brands.value?.length || 0, icon: '⚒️', color: '#06b6d4', key: 'nav.brands' },
    { label: 'Curations', value: categories.value?.length || 0, icon: '🏺', color: '#f59e0b', key: 'nav.categories' },
    { label: 'Boutiques', value: stores.value?.length || 0, icon: '💎', color: '#22c55e', key: 'nav.stores' },
])

onMounted(() => {
    fetchData()
})

watch(loading, (newVal) => {
    if (!newVal && !error.value) {
        nextTick(() => {
            gsap.from('.stat-card', {
                y: 30,
                opacity: 0,
                stagger: 0.1,
                duration: 0.5,
                ease: 'power2.out'
            })
            
            gsap.from('.product-row', {
                x: -20,
                opacity: 0,
                stagger: 0.05,
                duration: 0.4,
                delay: 0.3
            })
        })
    }
})
</script>

<template>
    <div>
            <header class="admin-header">
                <div>
                    <h1>{{ translateLanguage('admin.dashboard') }}</h1>
                    <p class="subtitle">{{ translateLanguage('admin.welcome_back') }} {{ auth.user?.username || translateLanguage('common.admin') }}</p>
                </div>
                <button class="btn btn-outline" @click="auth.logout()">{{ translateLanguage('common.logout') }}</button>
            </header>
            
            <!-- Loading State -->
            <div v-if="loading" class="loading-overlay">
                <Spinner size="lg" color="var(--primary)" />
                <p>{{ translateLanguage('admin.loading_data') }}</p>
            </div>
 
            <!-- Error State -->
            <div v-else-if="error" class="error-container">
                <div class="error-card">
                    <h3>{{ translateLanguage('admin.failed_load') }}</h3>
                    <p>{{ translateLanguage('admin.error_desc') || translateLanguage('common.error_desc') }}</p>
                    <button class="btn btn-primary" @click="fetchData">{{ translateLanguage('admin.retry') }}</button>
                    <div v-if="error.message || error.statusText" class="error-details">
                        {{ error.message || error.statusText || error }}
                    </div>
                </div>
            </div>

            <template v-else>
                <!-- Stats Grid -->
                <div class="stats-grid">
                    <div class="stat-card" style="--accent: var(--primary)">
                        <div class="stat-icon">💰</div>
                        <div class="stat-info">
                            <span class="stat-value">{{ totalRevenue.toLocaleString() }} {{ translateLanguage('common.currency') }}</span>
                            <span class="stat-label">{{ translateLanguage('admin.total_revenue') }}</span>
                        </div>
                    </div>
                    <div v-for="stat in stats" :key="stat.label" class="stat-card" :style="{ '--accent': stat.color }">
                        <div class="stat-icon">{{ stat.icon }}</div>
                        <div class="stat-info">
                            <span class="stat-value">{{ stat.value }}</span>
                            <span class="stat-label">{{ translateLanguage(stat.key) }}</span>
                        </div>
                    </div>
                </div>

                <div class="dashboard-grid">
                    <!-- Sales Chart -->
                    <section class="section chart-section">
                        <h3>{{ translateLanguage('admin.weekly_sales') }}</h3>
                        <AdminSalesChart :orders="orders || []" />
                    </section>

                    <!-- Low Stock Alert -->
                    <section class="section alert-section">
                        <h3>{{ translateLanguage('admin.low_stock_alerts') }} ({{ lowStockProducts.length }})</h3>
                        <div v-if="lowStockProducts.length > 0" class="alert-list">
                            <div v-for="p in lowStockProducts.slice(0, 5)" :key="p.id" class="alert-item">
                                <span>{{ p.name }}</span>
                                <span class="badge badge-warning">{{ p.stock }} {{ translateLanguage('common.left') }}</span>
                            </div>
                        </div>
                        <div v-else class="text-muted">{{ translateLanguage('admin.healthy_stock') }}</div>
                    </section>
                </div>
            </template>
            
            <!-- Recent Creations -->
            <section class="section">
                <div class="section-header">
                    <h2>{{ translateLanguage('admin.recent_products') }}</h2>
                    <div class="flex gap-2">
                        <NuxtLink to="/admin/users" class="btn btn-sm btn-outline">👑 {{ translateLanguage('admin.manage_admins') }}</NuxtLink>
                        <NuxtLink to="/admin/products" class="btn btn-sm btn-primary">+ {{ translateLanguage('admin.add_product') }}</NuxtLink>
                    </div>
                </div>
                
                <div class="table-container">
                    <div v-if="!products || products.length === 0" class="empty-state">
                        <p>{{ translateLanguage('admin.no_products') }}</p>
                        <NuxtLink to="/admin/products" class="btn btn-sm btn-primary">{{ translateLanguage('admin.add_product') }}</NuxtLink>
                    </div>
                    <table v-else class="data-table">
                        <thead>
                            <tr>
                                <th>{{ translateLanguage('admin.product') }}</th>
                                <th>{{ translateLanguage('admin.brand') }}</th>
                                <th>{{ translateLanguage('admin.price') }}</th>
                                <th>{{ translateLanguage('admin.stock') }}</th>
                                <th>{{ translateLanguage('admin.rating') }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="product in products?.slice(0, 5)" :key="product.id" class="product-row">
                                <td>
                                    <div class="product-cell">
                                        <img :src="product.image_url" :alt="product.name" class="product-thumb">
                                        <span>{{ product.name }}</span>
                                    </div>
                                </td>
                                <td>{{ product.brand?.name || '-' }}</td>
                                <td class="price">{{ (product.price || 0).toLocaleString() }} {{ translateLanguage('common.currency') }}</td>
                                <td>
                                    <span class="badge" :class="product.stock > 10 ? 'badge-success' : 'badge-warning'">
                                        {{ product.stock }}
                                    </span>
                                </td>
                                <td>⭐ {{ product.rating }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>
    </div>
</template>

<style scoped>
/* Keeping only page-specific styles */

.admin-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.subtitle {
    color: var(--text-muted);
    margin-top: 0.25rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.alert-item {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--border);
}

.stat-card {
    background: white;
    border-radius: 1.25rem;
    padding: 1.75rem;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    border: 1px solid var(--border);
    transition: all 0.3s;
}

.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.06);
    border-color: var(--accent);
}

.stat-icon {
    font-size: 2.25rem;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8fafc;
    border-radius: 1rem;
}

.stat-value {
    font-size: 1.75rem;
    font-weight: 800;
    display: block;
    color: #1e293b;
    line-height: 1.2;
}

.stat-label {
    color: var(--text-muted);
    font-size: 0.8125rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.025em;
}

.section {
    background: var(--surface);
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.table-container {
    overflow-x: auto;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th {
    text-align: left;
    padding: 1rem;
    border-bottom: 2px solid var(--border);
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.data-table td {
    padding: 1rem;
    border-bottom: 1px solid var(--border);
}

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

.price {
    font-weight: 600;
}

.badge {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-success {
    background: #dcfce7;
    color: #16a34a;
}

.badge-warning {
    background: #fef3c7;
    color: #d97706;
}

.empty-state {
    padding: 3rem;
    text-align: center;
    color: var(--text-muted);
}

.loading-overlay {
    padding: 10rem 0;
    text-align: center;
}

.error-container {
    padding: 5rem 0;
    display: flex;
    justify-content: center;
}

.error-card {
    background: white;
    padding: 3rem;
    border-radius: 1rem;
    text-align: center;
    max-width: 400px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.error-card h3 {
    color: #ef4444;
    margin-bottom: 1rem;
}

.error-card p {
    color: var(--text-muted);
    margin-bottom: 2rem;
}

.error-details {
    margin-top: 2rem;
    font-size: 0.75rem;
    color: #ef4444;
    font-family: monospace;
    opacity: 0.7;
}
</style>
