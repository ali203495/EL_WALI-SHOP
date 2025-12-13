<script setup lang="ts">
const api = useApi()

definePageMeta({
    layout: 'account',
    middleware: 'auth'
})

const { data: orders, pending } = await api.getOrders()
</script>

<template>
    <div class="orders-page">
        <header class="section-header">
            <h1>سجل الطلبات</h1>
        </header>

        <div v-if="pending" class="loading">
            جاري التحميل...
        </div>

        <div v-else-if="orders && orders.length > 0" class="orders-table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>رقم الطلب</th>
                        <th>التاريخ</th>
                        <th>الحالة</th>
                        <th>الإجمالي</th>
                        <!-- <th>الإجراءات</th> -->
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="order in orders" :key="order.id">
                        <td class="font-mono">#{{ order.id }}</td>
                        <td>{{ new Date(order.created_at || '').toLocaleDateString('ar-SA') }}</td>
                        <td>
                            <span class="status-badge" :class="order.status">{{ order.status }}</span>
                        </td>
                        <td class="font-bold">{{ order.total_amount?.toLocaleString() }} ريال</td>
                        <!-- <td><button class="btn-text">عرض التفاصيل</button></td> -->
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="empty-state">
            <p>لا توجد طلبات سابقة.</p>
            <NuxtLink to="/catalog" class="btn btn-primary mt-4">تسوق الآن</NuxtLink>
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
    text-align: right;
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
