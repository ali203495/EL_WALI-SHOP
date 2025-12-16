<script setup lang="ts">
const props = defineProps<{
    value: number
    max?: number
    showLabel?: boolean
    color?: 'primary' | 'success' | 'warning' | 'danger'
    size?: 'sm' | 'md' | 'lg'
}>()

const percentage = computed(() => {
    const max = props.max || 100
    return Math.min(100, Math.max(0, (props.value / max) * 100))
})
</script>

<template>
    <div class="progress-container">
        <div 
            class="progress-bar" 
            :class="[`progress-${color || 'primary'}`, `progress-${size || 'md'}`]"
        >
            <div 
                class="progress-fill" 
                :style="{ width: `${percentage}%` }"
            ></div>
        </div>
        <span v-if="showLabel" class="progress-label">{{ percentage.toFixed(0) }}%</span>
    </div>
</template>

<style scoped>
.progress-container {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.progress-bar {
    flex: 1;
    background: #e2e8f0;
    border-radius: 9999px;
    overflow: hidden;
}

.progress-sm { height: 4px; }
.progress-md { height: 8px; }
.progress-lg { height: 12px; }

.progress-fill {
    height: 100%;
    border-radius: 9999px;
    transition: width 0.3s ease;
}

.progress-primary .progress-fill { background: var(--primary); }
.progress-success .progress-fill { background: #22c55e; }
.progress-warning .progress-fill { background: #f59e0b; }
.progress-danger .progress-fill { background: #ef4444; }

.progress-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    min-width: 40px;
}
</style>
