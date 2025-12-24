<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import gsap from 'gsap'
import AdminSalesChart from '~/components/admin/SalesChart.vue'

definePageMeta({
    layout: 'admin'
})

const auth = useAuthStore()
const api = useApi()

// Fetch dashboard stats
const [
    { data: products },
    { data: brands },
    { data: stores },
    { data: categories },
    { data: orders }
] = await Promise.all([
    api.getProducts(),
    api.getBrands(),
    api.getStores(),
    api.getCategories(),
    api.getOrders()
])

const productsData = products
const brandsData = brands
const storesData = stores
const categoriesData = categories
const ordersData = orders

// Calculate Total Revenue
const totalRevenue = computed(() => {
    return ordersData.value?.reduce((acc: number, order: any) => acc + (order.total_amount || 0), 0) || 0
})

// Low Stock Items
const lowStockProducts = computed(() => {
    return productsData.value?.filter(p => p.stock <= 5) || []
})

const stats = computed(() => [
    { label: 'Products', value: products.value?.length || 0, icon: '📦', color: '#4f46e5' },
    { label: 'Brands', value: brands.value?.length || 0, icon: '🏷️', color: '#06b6d4' },
    { label: 'Categories', value: categories.value?.length || 0, icon: '📁', color: '#f59e0b' },
    { label: 'Stores', value: stores.value?.length || 0, icon: '🏪', color: '#22c55e' },
])

onMounted(() => {
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
</script>

<template>
    <div dir="rtl">
            <header class="admin-header">
                <div>
                    <h1>لوحة التحكم</h1>
                    <p class="subtitle">مرحبًا بعودتك، {{ auth.user?.username || 'Admin' }}</p>
                </div>
                <button @click="auth.logout()" class="btn btn-outline">تسجيل الخروج</button>
            </header>
            
            <!-- Stats Grid -->
            <div class="stats-grid">
                <div class="stat-card" style="--accent: #4f46e5">
                    <div class="stat-icon">💰</div>
                    <div class="stat-info">
                        <span class="stat-value">{{ totalRevenue.toLocaleString() }} د.إ</span>
                        <span class="stat-label">Total Revenue</span>
                    </div>
                </div>
                <div v-for="stat in stats" :key="stat.label" class="stat-card" :style="{ '--accent': stat.color }">
                    <div class="stat-icon">{{ stat.icon }}</div>
                    <div class="stat-info">
                        <span class="stat-value">{{ stat.value }}</span>
                        <span class="stat-label">{{ stat.label === 'Products' ? 'المنتجات' : stat.label === 'Brands' ? 'brands' : stat.label === 'Categories' ? 'Categories' : 'Stores' }}</span>
                    </div>
                </div>
            </div>

            <div class="dashboard-grid">
                <!-- Sales Chart -->
                <section class="section chart-section">
                    <h3>Weekly Sales</h3>
                    <AdminSalesChart :orders="ordersData || []" />
                </section>

                <!-- Low Stock Alert -->
                <section class="section alert-section">
                    <h3>Low Stock Alerts ({{ lowStockProducts.length }})</h3>
                    <div v-if="lowStockProducts.length > 0" class="alert-list">
                        <div v-for="p in lowStockProducts.slice(0, 5)" :key="p.id" class="alert-item">
                            <span>{{ p.name }}</span>
                            <span class="badge badge-warning">{{ p.stock }} left</span>
                        </div>
                    </div>
                    <div v-else class="text-muted">All stocks are healthy! ✅</div>
                </section>
            </div>
            
            <!-- Recent Products -->
            <section class="section">
                <div class="section-header">
                    <h2>أحدث المنتجات</h2>
                    <div class="flex gap-2">
                        <NuxtLink to="/admin/users" class="btn btn-sm btn-outline">👤 إدارة المسؤولين</NuxtLink>
                        <NuxtLink to="/admin/products" class="btn btn-sm btn-primary">+ إضافة منتج</NuxtLink>
                    </div>
                </div>
                
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>المنتج</th>
                                <th>العلامة التجارية</th>
                                <th>السعر</th>
                                <th>المخزون</th>
                                <th>التقييم</th>
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
                                <td class="price">{{ product.price.toLocaleString() }} د.إ</td>
                                <td>
                                    <span class="badge" :class="product.stock > 50 ? 'badge-success' : 'badge-warning'">
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
    background: var(--surface);
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border-right: 4px solid var(--accent);
    border-left: none;
}

.stat-icon {
    font-size: 2rem;
}

.stat-value {
    font-size: 2rem;
    font-weight: 800;
    display: block;
}

.stat-label {
    color: var(--text-muted);
    font-size: 0.875rem;
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
    text-align: right;
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
</style>
