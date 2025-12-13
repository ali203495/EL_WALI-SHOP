<script setup lang="ts">
interface Option {
    value: string | number
    label: string
}

const props = defineProps<{
    modelValue: string | number | null
    options: Option[]
    label?: string
    placeholder?: string
    error?: string
    disabled?: boolean
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: string | number): void
}>()

const handleChange = (e: Event) => {
    emit('update:modelValue', (e.target as HTMLSelectElement).value)
}
</script>

<template>
    <div class="select-group" :class="{ 'has-error': error }">
        <label v-if="label" class="select-label">{{ label }}</label>
        <select
            :value="modelValue"
            :disabled="disabled"
            class="select-field"
            @change="handleChange"
        >
            <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
            <option 
                v-for="option in options" 
                :key="option.value" 
                :value="option.value"
            >
                {{ option.label }}
            </option>
        </select>
        <span v-if="error" class="select-error">{{ error }}</span>
    </div>
</template>

<style scoped>
.select-group {
    margin-bottom: 1.25rem;
}

.select-label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.select-field {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid var(--border);
    border-radius: var(--radius);
    font-size: 1rem;
    background: var(--input-bg);
    color: var(--text);
    border-color: var(--input-border);
    appearance: none;
    cursor: pointer;
    transition: border-color 0.2s, box-shadow 0.2s;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2364748b' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 1rem center;
    padding-right: 2.5rem;
}

.select-field:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
}

.select-field:disabled {
    background: #f1f5f9;
    cursor: not-allowed;
}

.select-error {
    display: block;
    color: #ef4444;
    font-size: 0.75rem;
    margin-top: 0.5rem;
}

.has-error .select-field {
    border-color: #ef4444;
}
</style>
