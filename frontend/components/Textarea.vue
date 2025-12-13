<script setup lang="ts">
const props = defineProps<{
    modelValue: string
    label?: string
    placeholder?: string
    rows?: number
    error?: string
    disabled?: boolean
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
}>()

const handleInput = (e: Event) => {
    emit('update:modelValue', (e.target as HTMLTextAreaElement).value)
}
</script>

<template>
    <div class="textarea-group" :class="{ 'has-error': error }">
        <label v-if="label" class="textarea-label">{{ label }}</label>
        <textarea
            :value="modelValue"
            :placeholder="placeholder"
            :rows="rows || 4"
            :disabled="disabled"
            class="textarea-field"
            @input="handleInput"
        ></textarea>
        <span v-if="error" class="textarea-error">{{ error }}</span>
    </div>
</template>

<style scoped>
.textarea-group {
    margin-bottom: 1.25rem;
}

.textarea-label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.textarea-field {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid var(--border);
    border-radius: var(--radius);
    font-size: 1rem;
    font-family: inherit;
    resize: vertical;
    min-height: 100px;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.textarea-field:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
}

.textarea-field:disabled {
    background: #f1f5f9;
    cursor: not-allowed;
}

.textarea-error {
    display: block;
    color: #ef4444;
    font-size: 0.75rem;
    margin-top: 0.5rem;
}

.has-error .textarea-field {
    border-color: #ef4444;
}
</style>
