<script setup lang="ts">
defineProps<{
    title?: string
    padding?: 'sm' | 'md' | 'lg' | 'none'
    hoverable?: boolean
}>()
</script>

<template>
    <div 
        class="card" 
        :class="[
            `card-padding-${padding || 'md'}`,
            { 'card-hoverable': hoverable }
        ]"
    >
        <div v-if="title || $slots.header" class="card-header">
            <h3 v-if="title">{{ title }}</h3>
            <slot name="header" />
        </div>
        <div class="card-body">
            <slot />
        </div>
        <div v-if="$slots.footer" class="card-footer">
            <slot name="footer" />
        </div>
    </div>
</template>

<style scoped>
.card {
    background: white;
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.card-padding-none { padding: 0; }
.card-padding-sm .card-body { padding: 1rem; }
.card-padding-md .card-body { padding: 1.5rem; }
.card-padding-lg .card-body { padding: 2rem; }

.card-hoverable {
    transition: all 0.2s;
    cursor: pointer;
}

.card-hoverable:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.card-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-header h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
}

.card-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border);
    background: #f8fafc;
}
</style>
