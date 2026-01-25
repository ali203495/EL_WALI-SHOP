<script setup lang="ts">
const { translateLanguage, locale } = useLanguage()
const auth = useAuthStore()
const api = useApi()

definePageMeta({
    layout: 'account',
    middleware: ['auth']
})

// Fetch recent orders
const recentOrders = ref<any[]>([])
const loading = ref(true)
const error = ref<any>(null)

const fetchData = async () => {
    loading.value = true
    error.value = null
    try {
        const { data, error: apiError } = await api.getOrders()
        if (apiError.value) {
            error.value = apiError.value
            return
        }
        recentOrders.value = data.value || []
    } catch (e) {
        error.value = e
    } finally {
        loading.value = false
    }
}

const handleRetry = () => {
    fetchData()
}

onMounted(() => {
    fetchData()
})

const displayOrders = computed(() => {
    return recentOrders.value?.slice(0, 3) || []
})
</script>

<template>
    <div class="account-dashboard">
        <header class="section-header">
            <h1>{{ translateLanguage('account.welcome') }}, {{ auth.user?.first_name }}</h1>
            <p>{{ translateLanguage('account.dashboard_desc') }}</p>
        </header>

        <!-- Loading State -->
        <PageLoading v-if="loading" :message="translateLanguage('account.loading')" />

        <!-- Error State -->
        <ErrorState 
            v-else-if="error"
            :title="translateLanguage('admin.failed_load')"
            :description="translateLanguage('common.error_desc')"
            :retryable="true"
            @retry="handleRetry"
        >
            <template #footer>
                <div class="error-details">
                    {{ error.message || error.statusText || error }}
                </div>
            </template>
        </ErrorState>

        <template v-else>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="icon">✧</span>
                    <div class="info">
                        <span class="value">{{ recentOrders.length }}</span>
                        <span class="label">{{ translateLanguage('account.total_orders') }}</span>
                    </div>
                </div>
            </div>

            <section class="recent-orders mt-8">
                <div class="section-title">
                    <h2>{{ translateLanguage('account.recent_orders') }}</h2>
                    <NuxtLink to="/account/orders" class="view-all">{{ translateLanguage('account.view_all') }}</NuxtLink>
                </div>
                
                <div v-if="displayOrders.length > 0" class="orders-list">
                    <div v-for="order in displayOrders" :key="order.id" class="order-card">
                        <div class="order-header">
                            <span class="order-id">#{{ order.id }}</span>
                            <span class="order-date">{{ new Date(order.created_at || '').toLocaleDateString(locale === 'ar' ? 'ar-SA' : locale === 'fr' ? 'fr-FR' : 'en-US') }}</span>
                        </div>
                        <div class="order-info">
                            <div class="status">
                                <span class="status-badge" :class="order.status">{{ order.status }}</span>
                            </div>
                            <div class="total">
                                {{ order.total_amount?.toLocaleString() }} {{ translateLanguage('common.currency') }}
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="empty-state">
                    <p>{{ translateLanguage('account.no_orders') }}</p>
                    <NuxtLink to="/catalog" class="btn btn-primary btn-sm">{{ translateLanguage('wishlist.browse') }}</NuxtLink>
                </div>
            </section>
        </template>
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
