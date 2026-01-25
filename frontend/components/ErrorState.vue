<script setup lang="ts">
const { translateLanguage } = useLanguage()

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
        <h3>{{ title || translateLanguage('common.error_title') }}</h3>
        <p>{{ description || translateLanguage('common.error_desc') }}</p>
        <div class="error-actions">
            <button v-if="retryable" class="btn btn-primary" @click="emit('retry')">
                {{ translateLanguage('common.try_again') }}
            </button>
            <NuxtLink to="/" class="btn btn-outline">
                {{ translateLanguage('common.go_home') }}
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
