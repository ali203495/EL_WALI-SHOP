<script setup lang="ts">
defineProps<{
    message?: string
}>()
</script>

<template>
    <div class="page-loading">
        <div class="loading-content">
            <div class="logo-pulse">
                <span class="logo-text">MAISON <span class="highlight">EL WALI</span></span>
            </div>
            <Spinner size="lg" />
            <p v-if="message">{{ message }}</p>
        </div>
    </div>
</template>

<style scoped>
.page-loading {
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.loading-content {
    text-align: center;
}

.logo-pulse {
    margin-bottom: 2rem;
    animation: pulse 2s ease-in-out infinite;
}

.logo-text {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.highlight {
    color: var(--primary);
}

p {
    margin-top: 1.5rem;
    color: var(--text-muted);
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}
</style>
