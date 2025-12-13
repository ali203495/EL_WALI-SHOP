<script setup lang="ts">
defineProps<{
    icon?: string
    title: string
    description?: string
}>()
</script>

<template>
    <div class="empty-state">
        <span class="empty-icon">{{ icon || '📭' }}</span>
        <h3>{{ title }}</h3>
        <p v-if="description">{{ description }}</p>
        <div class="empty-actions">
            <slot name="actions" />
        </div>
    </div>
</template>

<style scoped>
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
}

.empty-icon {
    font-size: 4rem;
    display: block;
    margin-bottom: 1.5rem;
}

h3 {
    color: var(--text);
    margin-bottom: 0.5rem;
}

p {
    max-width: 400px;
    margin: 0 auto 1.5rem;
}

.empty-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
}
</style>
