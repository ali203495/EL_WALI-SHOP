<script setup lang="ts">
interface ChartData {
    label: string
    value: number
}

defineProps<{
    data: ChartData[]
    title?: string
    color?: string
}>()

const maxValue = computed(() => {
    return Math.max(...(props.data?.map(d => d.value) || [0]))
})
</script>

<template>
    <div class="chart-container">
        <h4 v-if="title" class="chart-title">{{ title }}</h4>
        <div class="chart-bars">
            <div v-for="item in data" :key="item.label" class="chart-bar-group">
                <div class="chart-bar-wrapper">
                    <div 
                        class="chart-bar" 
                        :style="{ 
                            height: `${(item.value / maxValue) * 100}%`,
                            background: color || 'var(--primary)'
                        }"
                    ></div>
                </div>
                <span class="chart-label">{{ item.label }}</span>
                <span class="chart-value">{{ item.value }}</span>
            </div>
        </div>
    </div>
</template>

<style scoped>
.chart-container {
    background: white;
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
}

.chart-title {
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    color: var(--text-muted);
}

.chart-bars {
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    height: 150px;
    gap: 0.5rem;
}

.chart-bar-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
}

.chart-bar-wrapper {
    width: 100%;
    max-width: 40px;
    height: 120px;
    display: flex;
    align-items: flex-end;
}

.chart-bar {
    width: 100%;
    min-height: 4px;
    border-radius: 4px 4px 0 0;
    transition: height 0.5s ease;
}

.chart-label {
    font-size: 0.65rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
    text-transform: uppercase;
}

.chart-value {
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.25rem;
}
</style>
