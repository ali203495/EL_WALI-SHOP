<script setup lang="ts">
import gsap from 'gsap'

definePageMeta({
    layout: 'admin'
})

const api = useApi()
const { data: orders } = await api.getOrders()

const formatDate = (date: string) => {
    return new Date(date).toLocaleString('ar-EG', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

const totalRevenue = computed(() => {
    return (orders.value || []).reduce((sum, o) => sum + o.total_amount, 0) || 0
})

onMounted(() => {
    gsap.from('.order-row', {
        x: -20,
        opacity: 0,
        stagger: 0.05,
        duration: 0.4
    })
})
</script>

<template>
    <div dir="rtl">
        <header class="page-header">
                <div>
                    <h1>الطلبات</h1>
                    <p class="subtitle">عرض سجل الطلبات والمعاملات</p>
                </div>
            </header>

            <!-- Stats -->
            <div class="stats-row">
                <div class="stat-card">
                    <span class="stat-icon">📦</span>
                    <div>
                        <span class="stat-value">{{ (orders || []).length }}</span>
                        <span class="stat-label">إجمالي الطلبات</span>
                    </div>
                </div>
                <div class="stat-card">
                    <span class="stat-icon">💰</span>
                    <div>
                        <span class="stat-value">{{ totalRevenue.toLocaleString() }} د.إ</span>
                        <span class="stat-label">إجمالي الإيرادات</span>
                    </div>
                </div>
                <div class="stat-card">
                    <span class="stat-icon">📈</span>
                    <div>
                        <span class="stat-value">{{ (orders?.length ? (totalRevenue / orders.length) : 0).toFixed(2) }} د.إ</span>
                        <span class="stat-label">متوسط قيمة الطلب</span>
                    </div>
                </div>
            </div>

            <!-- Orders Table -->
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>رقم الطلب</th>
                            <th>التاريخ</th>
                            <th>العناصر</th>
                            <th>الإجمالي</th>
                            <th>الحالة</th>
                            <th>الإجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="order in orders" :key="order.id" class="order-row">
                            <td class="order-id">#{{ order.id.toString().padStart(4, '0') }}</td>
                            <td>{{ formatDate(order.created_at) }}</td>
                            <td>{{ order.items?.length || 0 }} عناصر</td>
                            <td class="order-total">{{ order.total_amount.toLocaleString() }} د.إ</td>
                            <td>
                                <span class="status-badge" :class="order.status.toLowerCase()">
                                    {{ order.status === 'completed' ? 'مكتمل' : (order.status === 'pending' ? 'قيد الانتظار' : order.status) }}
                                </span>
                            </td>
                            <td>
                                <button class="action-btn" title="View Details" @click="api.getOrders()">👁️</button>
                                <button class="action-btn" title="Print Receipt" @click="api.getOrders()">🖨️</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
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

/* Global table styles used */
.order-id { font-family: monospace; font-weight: 600; }
.order-total { font-weight: 700; }

.status-badge {
    /* Component specific overrides */
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
