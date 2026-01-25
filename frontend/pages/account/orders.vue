<script setup lang="ts">
const { translateLanguage, locale } = useLanguage()
const api = useApi()

definePageMeta({
    layout: 'account',
    middleware: ['auth']
})

const orders = ref<any[]>([])
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
        orders.value = data.value || []
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
</script>

<template>
    <div class="orders-page">
        <header class="section-header">
            <h1>{{ translateLanguage('account.order_history') }}</h1>
        </header>

        <PageLoading v-if="loading" :message="translateLanguage('account.loading')" />

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

        <div v-else-if="orders.length > 0" class="orders-table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>{{ translateLanguage('account.order_id') }}</th>
                        <th>{{ translateLanguage('account.date') }}</th>
                        <th>{{ translateLanguage('account.status') }}</th>
                        <th>{{ translateLanguage('account.total') }}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="order in orders" :key="order.id">
                        <td class="font-mono">#{{ order.id }}</td>
                        <td>{{ new Date(order.created_at || '').toLocaleDateString(locale === 'ar' ? 'ar-SA' : locale === 'fr' ? 'fr-FR' : 'en-US') }}</td>
                        <td>
                            <span class="status-badge" :class="order.status">{{ order.status }}</span>
                        </td>
                        <td class="font-bold">{{ order.total_amount?.toLocaleString() }} {{ translateLanguage('common.currency') }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="empty-state">
            <p>{{ translateLanguage('account.no_previous_orders') }}</p>
            <NuxtLink to="/catalog" class="btn btn-primary mt-4">{{ translateLanguage('account.shop_now') }}</NuxtLink>
        </div>
    </div>
</template>

<style scoped>
.section-header {
    margin-bottom: 2rem;
}

.orders-table-container {
    overflow-x: auto;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 600px;
}

.data-table th,
.data-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

.data-table th {
    background: #f8fafc;
    font-weight: 600;
    color: var(--text-muted);
}

.status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 99px;
    font-size: 0.75rem;
    background: #f1f5f9;
    display: inline-block;
}

.status-badge.completed {
    background: #dcfce7;
    color: #166534;
}

.empty-state {
    text-align: center;
    padding: 4rem 1rem;
    background: #f8fafc;
    border-radius: var(--radius);
}

.font-mono { font-family: monospace; }
.font-bold { font-weight: 700; }
.mt-4 { margin-top: 1rem; }
</style>
