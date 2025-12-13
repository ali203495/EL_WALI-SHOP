<script setup lang="ts">
const auth = useAuthStore()
const api = useApi()

definePageMeta({
    layout: 'account',
    middleware: 'auth'
})

// Fetch recent orders
const { data: recentOrders } = await api.getOrders()

// Filter to top 3 logic if backend returns all (though backend now filters)
// But to be safe and efficient UI
const displayOrders = computed(() => {
    return recentOrders.value?.slice(0, 3) || []
})
</script>

<template>
    <div class="account-dashboard">
        <header class="section-header">
            <h1>مرحباً، {{ auth.user?.first_name }} 👋</h1>
            <p>هذه لوحة التحكم الخاصة بك. يمكنك متابعة طلباتك وتحديث بياناتك.</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <span class="icon">📦</span>
                <div class="info">
                    <span class="value">{{ recentOrders?.length || 0 }}</span>
                    <span class="label">إجمالي الطلبات</span>
                </div>
            </div>
            <!-- Add more stats if needed -->
        </div>

        <section class="recent-orders mt-8">
            <div class="section-title">
                <h2>أحدث الطلبات</h2>
                <NuxtLink to="/account/orders" class="view-all">عرض الكل</NuxtLink>
            </div>
            
            <div v-if="displayOrders.length > 0" class="orders-list">
                <div v-for="order in displayOrders" :key="order.id" class="order-card">
                    <div class="order-header">
                        <span class="order-id">#{{ order.id }}</span>
                        <span class="order-date">{{ new Date(order.created_at || '').toLocaleDateString('ar-SA') }}</span>
                    </div>
                    <div class="order-info">
                        <div class="status">
                            <span class="status-badge" :class="order.status">{{ order.status }}</span>
                        </div>
                        <div class="total">
                            {{ order.total_amount?.toLocaleString() }} ريال
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="empty-state">
                <p>لا توجد طلبات حتى الآن.</p>
                <NuxtLink to="/catalog" class="btn btn-primary btn-sm">تصفح المنتجات</NuxtLink>
            </div>
        </section>
    </div>
</template>

<style scoped>
.section-header h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.section-header p {
    color: var(--text-muted);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.stat-card {
    background: #f8fafc;
    padding: 1.5rem;
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    gap: 1rem;
    border: 1px solid var(--border);
}

.stat-card .icon {
    font-size: 2rem;
    background: white;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.stat-card .value {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}

.stat-card .label {
    font-size: 0.875rem;
    color: var(--text-muted);
}

.mt-8 { margin-top: 3rem; }

.section-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.view-all {
    color: var(--primary);
    text-decoration: none;
    font-size: 0.875rem;
    font-weight: 600;
}

.order-card {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    margin-bottom: 1rem;
    background: white;
    transition: transform 0.2s, box-shadow 0.2s;
}

.order-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}

.order-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.order-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 99px;
    font-size: 0.75rem;
    background: #f1f5f9;
}

.status-badge.completed {
    background: #dcfce7;
    color: #166534;
}

.empty-state {
    text-align: center;
    padding: 3rem;
    background: #f8fafc;
    border-radius: var(--radius);
    color: var(--text-muted);
}
</style>
