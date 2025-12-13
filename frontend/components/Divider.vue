<script setup lang="ts">
defineProps<{
    text?: string
    vertical?: boolean
}>()
</script>

<template>
    <div class="divider" :class="{ 'divider-vertical': vertical }">
        <span v-if="text" class="divider-text">{{ text }}</span>
    </div>
</template>

<style scoped>
.divider {
    display: flex;
    align-items: center;
    width: 100%;
    margin: 1.5rem 0;
}

.divider::before,
.divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

.divider-text {
    padding: 0 1rem;
    color: var(--text-muted);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.divider-vertical {
    width: 1px;
    height: 100%;
    margin: 0 1.5rem;
    flex-direction: column;
}

.divider-vertical::before,
.divider-vertical::after {
    width: 1px;
    height: auto;
    flex: 1;
}
</style>
