<script setup lang="ts">
// Redirect to catalog (Collections)
navigateTo('/catalog')
</script>

<template>
    <div class="redirect-message">
        <p>Redirecting to Collections...</p>
    </div>
</template>

<style scoped>
.redirect-message {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    color: var(--text-muted);
}
</style>
