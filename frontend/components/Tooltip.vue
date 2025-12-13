<script setup lang="ts">
defineProps<{
    text: string
    position?: 'top' | 'bottom' | 'left' | 'right'
}>()
</script>

<template>
    <div class="tooltip-wrapper" :class="[`tooltip-${position || 'top'}`]">
        <slot />
        <span class="tooltip-text">{{ text }}</span>
    </div>
</template>

<style scoped>
.tooltip-wrapper {
    position: relative;
    display: inline-block;
}

.tooltip-text {
    visibility: hidden;
    opacity: 0;
    position: absolute;
    background: #0f172a;
    color: white;
    padding: 0.5rem 0.75rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
    white-space: nowrap;
    z-index: 100;
    transition: opacity 0.2s, visibility 0.2s;
}

.tooltip-wrapper:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
}

/* Positions */
.tooltip-top .tooltip-text {
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    margin-bottom: 0.5rem;
}

.tooltip-bottom .tooltip-text {
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 0.5rem;
}

.tooltip-left .tooltip-text {
    right: 100%;
    top: 50%;
    transform: translateY(-50%);
    margin-right: 0.5rem;
}

.tooltip-right .tooltip-text {
    left: 100%;
    top: 50%;
    transform: translateY(-50%);
    margin-left: 0.5rem;
}
</style>
