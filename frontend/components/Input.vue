<script setup lang="ts">
const props = defineProps<{
    modelValue: string | number
    label?: string
    type?: string
    placeholder?: string
    error?: string
    disabled?: boolean
    icon?: string
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: string | number): void
}>()

const handleInput = (e: Event) => {
    emit('update:modelValue', (e.target as HTMLInputElement).value)
}
</script>

<template>
    <div class="input-group" :class="{ 'has-error': error }">
        <label v-if="label" class="input-label">{{ label }}</label>
        <div class="input-wrapper">
            <span v-if="icon" class="input-icon">{{ icon }}</span>
            <input
                :type="type || 'text'"
                :value="modelValue"
                :placeholder="placeholder"
                :disabled="disabled"
                class="input-field"
                :class="{ 'with-icon': icon }"
                @input="handleInput"
            />
        </div>
        <span v-if="error" class="input-error">{{ error }}</span>
    </div>
</template>

<style scoped>
.input-group {
    margin-bottom: 1.25rem;
}

.input-label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.input-wrapper {
    position: relative;
}

.input-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1rem;
    color: var(--text-muted);
}

.input-field.with-icon {
    padding-left: 2.75rem;
}

.input-error {
    display: block;
    color: #ef4444;
    font-size: 0.75rem;
    margin-top: 0.5rem;
}

.has-error .input-field {
    border-color: #ef4444;
}

.has-error .input-field:focus {
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
}
</style>
