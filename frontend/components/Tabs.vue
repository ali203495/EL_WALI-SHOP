<script setup lang="ts">
interface Tab {
    id: string
    label: string
    icon?: string
}

const props = defineProps<{
    tabs: Tab[]
    modelValue: string
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', id: string): void
}>()

const selectTab = (id: string) => {
    emit('update:modelValue', id)
}
</script>

<template>
    <div class="tabs-container">
        <div class="tabs-header">
            <button
                v-for="tab in tabs"
                :key="tab.id"
                class="tab-button"
                :class="{ active: modelValue === tab.id }"
                @click="selectTab(tab.id)"
            >
                <span v-if="tab.icon" class="tab-icon">{{ tab.icon }}</span>
                {{ tab.label }}
            </button>
        </div>
        <div class="tabs-content">
            <slot :name="modelValue" />
        </div>
    </div>
</template>

<style scoped>
.tabs-container {
    width: 100%;
}

.tabs-header {
    display: flex;
    border-bottom: 2px solid var(--border);
    gap: 0.5rem;
}

.tab-button {
    padding: 0.75rem 1.25rem;
    background: none;
    border: none;
    font-size: 0.9375rem;
    font-weight: 500;
    color: var(--text-muted);
    cursor: pointer;
    position: relative;
    transition: color 0.2s;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.tab-button:hover {
    color: var(--text);
}

.tab-button.active {
    color: var(--primary);
}

.tab-button.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--primary);
}

.tab-icon {
    font-size: 1rem;
}

.tabs-content {
    padding: 1.5rem 0;
}
</style>
