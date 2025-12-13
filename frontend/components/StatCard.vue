<script setup lang="ts">
defineProps<{
    label: string
    value: number | string
    icon: string
    color?: string
}>()
</script>

<template>
    <div class="stat-card" :style="{ '--accent-color': color || 'var(--primary)' }">
        <div class="stat-icon">{{ icon }}</div>
        <div class="stat-content">
            <span class="stat-value">{{ typeof value === 'number' ? value.toLocaleString() : value }}</span>
            <span class="stat-label">{{ label }}</span>
        </div>
    </div>
</template>

<style scoped>
.stat-card {
    background: white;
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border-left: 4px solid var(--accent-color);
}

.stat-icon {
    font-size: 2rem;
}

.stat-content {
    display: flex;
    flex-direction: column;
}

.stat-value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
}

.stat-label {
    color: var(--text-muted);
    font-size: 0.875rem;
    margin-top: 0.25rem;
}
</style>
