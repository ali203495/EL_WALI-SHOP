<script setup lang="ts">
defineProps<{
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
    size?: 'sm' | 'md' | 'lg'
    loading?: boolean
    disabled?: boolean
    block?: boolean
}>()
</script>

<template>
    <button 
        class="btn" 
        :class="[
            `btn-${variant || 'primary'}`,
            `btn-${size || 'md'}`,
            { 'btn-block': block, 'btn-loading': loading }
        ]"
        :disabled="disabled || loading"
    >
        <span v-if="loading" class="btn-spinner"></span>
        <slot />
    </button>
</template>

<style scoped>
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    font-weight: 600;
    border-radius: var(--radius);
    cursor: pointer;
    transition: all 0.2s;
    border: none;
}

/* Sizes */
.btn-sm { padding: 0.5rem 1rem; font-size: 0.875rem; }
.btn-md { padding: 0.75rem 1.5rem; font-size: 1rem; }
.btn-lg { padding: 1rem 2rem; font-size: 1.125rem; }

/* Variants */
.btn-primary {
    background: var(--primary);
    color: white;
}
.btn-primary:hover { background: var(--primary-hover); }

.btn-secondary {
    background: var(--secondary);
    color: white;
}
.btn-secondary:hover { opacity: 0.9; }

.btn-outline {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text);
}
.btn-outline:hover { border-color: var(--text); }

.btn-ghost {
    background: transparent;
    color: var(--text);
}
.btn-ghost:hover { background: #f1f5f9; }

.btn-danger {
    background: #ef4444;
    color: white;
}
.btn-danger:hover { background: #dc2626; }

/* States */
.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-block { width: 100%; }

.btn-loading { pointer-events: none; }

.btn-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid currentColor;
    border-top-color: transparent;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
</style>
