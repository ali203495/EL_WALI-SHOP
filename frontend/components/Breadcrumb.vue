<script setup lang="ts">
interface BreadcrumbItem {
    label: string
    to?: string
}

defineProps<{
    items: BreadcrumbItem[]
}>()
</script>

<template>
    <nav class="breadcrumb">
        <template v-for="(item, index) in items" :key="index">
            <NuxtLink v-if="item.to" :to="item.to" class="breadcrumb-link">
                {{ item.label }}
            </NuxtLink>
            <span v-else class="breadcrumb-current">{{ item.label }}</span>
            <span v-if="index < items.length - 1" class="breadcrumb-separator">/</span>
        </template>
    </nav>
</template>

<style scoped>
.breadcrumb {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: var(--text-muted);
}

.breadcrumb-link {
    color: var(--text-muted);
    text-decoration: none;
    transition: color 0.2s;
}

.breadcrumb-link:hover {
    color: var(--primary);
}

.breadcrumb-separator {
    opacity: 0.5;
}

.breadcrumb-current {
    color: var(--text);
    font-weight: 500;
}
</style>
