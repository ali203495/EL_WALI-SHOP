<script setup lang="ts">
defineProps<{
    size?: 'sm' | 'md' | 'lg'
    color?: string
}>()
</script>

<template>
    <div class="spinner-container">
        <div 
            class="spinner" 
            :class="[`spinner-${size || 'md'}`]"
            :style="{ borderTopColor: color || 'var(--primary)' }"
        ></div>
    </div>
</template>

<style scoped>
.spinner-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem;
}

.spinner {
    border-radius: 50%;
    border: 3px solid #e2e8f0;
    border-top-color: var(--primary);
    animation: spin 0.8s linear infinite;
}

.spinner-sm {
    width: 20px;
    height: 20px;
    border-width: 2px;
}

.spinner-md {
    width: 32px;
    height: 32px;
}

.spinner-lg {
    width: 48px;
    height: 48px;
    border-width: 4px;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
</style>
