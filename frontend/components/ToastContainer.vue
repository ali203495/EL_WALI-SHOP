<script setup lang="ts">
import { useToast } from '~/composables/useToast'

const { toasts, remove } = useToast()
</script>

<template>
    <Teleport to="body">
        <div class="toast-container">
            <TransitionGroup name="toast">
                <div 
                    v-for="toast in toasts" 
                    :key="toast.id" 
                    class="toast" 
                    :class="[`toast-${toast.type}`]"
                >
                    <span class="toast-icon">
                        <template v-if="toast.type === 'success'">✓</template>
                        <template v-else-if="toast.type === 'error'">✕</template>
                        <template v-else-if="toast.type === 'warning'">⚠</template>
                        <template v-else>ℹ</template>
                    </span>
                    <span class="toast-message">{{ toast.message }}</span>
                    <button class="toast-close" @click="remove(toast.id)">×</button>
                </div>
            </TransitionGroup>
        </div>
    </Teleport>
</template>

<style scoped>
.toast-container {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.toast {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    background: white;
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    min-width: 300px;
    max-width: 400px;
}

.toast-success {
    border-left: 4px solid #22c55e;
}

.toast-error {
    border-left: 4px solid #ef4444;
}

.toast-warning {
    border-left: 4px solid #f59e0b;
}

.toast-info {
    border-left: 4px solid #3b82f6;
}

.toast-icon {
    font-size: 1.25rem;
}

.toast-success .toast-icon { color: #22c55e; }
.toast-error .toast-icon { color: #ef4444; }
.toast-warning .toast-icon { color: #f59e0b; }
.toast-info .toast-icon { color: #3b82f6; }

.toast-message {
    flex: 1;
    font-size: 0.9375rem;
}

.toast-close {
    background: none;
    border: none;
    font-size: 1.25rem;
    cursor: pointer;
    color: #94a3b8;
}

.toast-close:hover {
    color: var(--secondary);
}

/* Animations */
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s ease;
}

.toast-enter-from {
    transform: translateX(100%);
    opacity: 0;
}

.toast-leave-to {
    transform: translateX(100%);
    opacity: 0;
}
</style>
