<script setup lang="ts">
import { gsap } from 'gsap'
const { translateLanguage, locale } = useLanguage()

definePageMeta({
    layout: 'admin'
})

const api = useApi()
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
    gsap.from('.order-row', {
        x: -20,
        opacity: 0,
        stagger: 0.05,
        duration: 0.4
    })
})

const formatDate = (date: string) => {
    if (!date) return '-'
    return new Date(date).toLocaleString(locale.value === 'ar' ? 'ar-EG' : (locale.value === 'fr' ? 'fr-FR' : 'en-US'), {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

const totalRevenue = computed(() => {
    return (orders.value || []).reduce((sum, o) => sum + o.total_amount, 0) || 0
})

const exportCSV = () => {
    if (!orders.value || orders.value.length === 0) return
    
    // Headers
    const headers = [
        translateLanguage('admin.order_id'),
        translateLanguage('admin.date'),
        translateLanguage('admin.customer'),
        translateLanguage('common.email'),
        translateLanguage('common.total'),
        translateLanguage('admin.status'),
        translateLanguage('admin.payment')
    ]
    
    // Rows
    const rows = orders.value.map(o => [
        o.id,
        new Date(o.created_at).toLocaleDateString(),
        `"${o.customer_name || translateLanguage('admin.guest')}"`,
        o.customer_email || '-',
        o.total_amount,
        o.status,
        o.payment_status || '-'
    ].join(','))
    
    const csvContent = [headers.join(','), ...rows].join('\n')
    
    // Download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `orders_${new Date().toISOString().slice(0,10)}.csv`
    link.click()
}
</script>

<template>
    <div>
        <header class="page-header">
                <div>
                    <h1>{{ translateLanguage('admin.orders_management') }}</h1>
                    <p class="subtitle">{{ translateLanguage('nav.admin_portal') }} / {{ translateLanguage('nav.orders') }}</p>
                </div>
                <div class="flex gap-2">
                    <button class="btn btn-outline" :title="translateLanguage('admin.export_csv')" @click="exportCSV">📥 {{ translateLanguage('admin.export_csv') }}</button>
                </div>
            </header>

            <!-- Loading State -->
            <PageLoading v-if="loading" :message="translateLanguage('admin.loading_data')" />

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
                <!-- Stats -->
                <div class="stats-row">
                    <div class="stat-card">
                        <span class="stat-icon">📜</span>
                        <div>
                            <span class="stat-value">{{ orders.length }}</span>
                            <span class="stat-label">{{ translateLanguage('nav.orders') }}</span>
                        </div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-icon">💰</span>
                        <div>
                            <span class="stat-value">{{ totalRevenue.toLocaleString() }} {{ translateLanguage('common.currency') }}</span>
                            <span class="stat-label">{{ translateLanguage('admin.total_revenue') }}</span>
                        </div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-icon">📈</span>
                        <div>
                            <span class="stat-value">{{ (orders.length ? (totalRevenue / orders.length) : 0).toLocaleString(undefined, { maximumFractionDigits: 0 }) }} {{ translateLanguage('common.currency') }}</span>
                            <span class="stat-label">{{ translateLanguage('admin.average_value') }}</span>
                        </div>
                    </div>
                </div>

                <!-- Orders Table -->
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>{{ translateLanguage('admin.order_id') }}</th>
                                <th>{{ translateLanguage('admin.date') }}</th>
                                <th>{{ translateLanguage('admin.items') }}</th>
                                <th>{{ translateLanguage('admin.price') }}</th>
                                <th>{{ translateLanguage('admin.status') }}</th>
                                <th>{{ translateLanguage('admin.actions') }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="order in orders" :key="order.id" class="order-row">
                                <td class="order-id">#{{ order.id.toString().padStart(4, '0') }}</td>
                                <td>{{ formatDate(order.created_at) }}</td>
                                <td>{{ order.items?.length || 0 }} {{ translateLanguage('admin.items') }}</td>
                                <td class="order-total">{{ order.total_amount.toLocaleString() }} {{ translateLanguage('common.currency') }}</td>
                                <td>
                                    <span class="status-badge" :class="order.status.toLowerCase()">
                                        {{ order.status === 'completed' ? translateLanguage('admin.completed') : (order.status === 'pending' ? translateLanguage('admin.pending') : order.status) }}
                                    </span>
                                </td>
                                <td>
                                    <button class="action-btn" :title="translateLanguage('admin.view_details')" @click="fetchData">👁️</button>
                                    <button class="action-btn" :title="translateLanguage('admin.print_receipt')" @click="fetchData">🖨️</button>
                                </td>
                            </tr>
                            <tr v-if="orders.length === 0">
                                <td colspan="6" style="text-align: center; padding: 3rem; color: var(--text-muted);">
                                    {{ translateLanguage('admin.no_data') }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </template>
    </div>
</template>

<style scoped>
/* Page specific styles */

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.subtitle {
    color: var(--text-muted);
    margin-top: 0.25rem;
}

.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stat-icon { font-size: 2rem; }
.stat-value { font-size: 1.5rem; font-weight: 800; display: block; }
.stat-label { color: var(--text-muted); font-size: 0.875rem; }

.table-container {
    background: white;
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
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

.order-row {
    transition: all 0.2s;
}

.order-row:hover {
    background: #fcfdfd;
}

/* Global table styles used */
.order-id { font-family: monospace; font-weight: 600; }
.order-total { font-weight: 700; }

.status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: capitalize;
}

.status-badge.completed {
    background: rgba(16, 185, 129, 0.1);
    color: var(--success);
}

.status-badge.pending {
     background: rgba(245, 158, 11, 0.1);
     color: var(--accent);
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

.action-btn:hover { background: #f1f5f9; }
</style>
