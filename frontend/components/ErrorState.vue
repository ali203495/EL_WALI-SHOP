<script setup lang="ts">
defineProps<{
    icon?: string
    title?: string
    description?: string
    retryable?: boolean
}>()

const emit = defineEmits<{
    (e: 'retry'): void
}>()
</script>

<template>
    <div class="error-state">
        <span class="error-icon">{{ icon || '⚠️' }}</span>
        <h3>{{ title || 'Something went wrong' }}</h3>
        <p>{{ description || 'We encountered an error while loading this content.' }}</p>
        <div class="error-actions">
            <button v-if="retryable" class="btn btn-primary" @click="emit('retry')">
                Try Again
            </button>
            <NuxtLink to="/" class="btn btn-outline">
                Go Home
            </NuxtLink>
        </div>
    </div>
</template>

<style scoped>
.error-state {
    text-align: center;
    padding: 4rem 2rem;
    max-width: 500px;
    margin: 0 auto;
}

.error-icon {
    font-size: 4rem;
    display: block;
    margin-bottom: 1.5rem;
}

h3 {
    color: var(--text);
    margin-bottom: 0.75rem;
    font-size: 1.5rem;
}

p {
    color: var(--text-muted);
    margin-bottom: 2rem;
    line-height: 1.6;
}

.error-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
}
</style>
