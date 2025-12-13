<script setup lang="ts">
const props = defineProps<{
    modelValue: boolean
    label?: string
    disabled?: boolean
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
}>()

const toggle = () => {
    if (!props.disabled) {
        emit('update:modelValue', !props.modelValue)
    }
}
</script>

<template>
    <label class="switch-container" :class="{ disabled }">
        <button 
            type="button"
            class="switch" 
            :class="{ active: modelValue }"
            :disabled="disabled"
            @click="toggle"
        >
            <span class="switch-thumb"></span>
        </button>
        <span v-if="label" class="switch-label">{{ label }}</span>
    </label>
</template>

<style scoped>
.switch-container {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    cursor: pointer;
}

.switch-container.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.switch {
    position: relative;
    width: 44px;
    height: 24px;
    background: #e2e8f0;
    border: none;
    border-radius: 9999px;
    cursor: pointer;
    transition: background 0.2s;
}

.switch.active {
    background: var(--primary);
}

.switch-thumb {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 20px;
    height: 20px;
    background: white;
    border-radius: 50%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    transition: transform 0.2s;
}

.switch.active .switch-thumb {
    transform: translateX(20px);
}

.switch-label {
    font-size: 0.9375rem;
    color: var(--text);
}
</style>
