<script setup lang="ts">
defineProps<{
    variant?: 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info'
    size?: 'sm' | 'md'
}>()
</script>

<template>
    <span 
        class="badge" 
        :class="[
            `badge-${variant || 'default'}`,
            `badge-${size || 'md'}`
        ]"
    >
        <slot />
    </span>
</template>

<style scoped>
.badge {
    display: inline-flex;
    align-items: center;
    font-weight: 600;
    border-radius: 9999px;
}

.badge-sm {
    padding: 0.125rem 0.5rem;
    font-size: 0.65rem;
}

.badge-md {
    padding: 0.25rem 0.75rem;
    font-size: 0.75rem;
}

.badge-default {
    background: #f1f5f9;
    color: #475569;
}

.badge-primary {
    background: var(--primary-light);
    color: var(--primary);
}

.badge-success {
    background: #dcfce7;
    color: #16a34a;
}

.badge-warning {
    background: #fef3c7;
    color: #d97706;
}

.badge-danger {
    background: #fef2f2;
    color: #dc2626;
}

.badge-info {
    background: #e0f2fe;
    color: #0284c7;
}
</style>
