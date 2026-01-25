<script setup lang="ts">
const { translateLanguage } = useLanguage()

defineProps<{
    modelValue: boolean
    title?: string
    message?: string
    confirmText?: string
    cancelText?: string
    danger?: boolean
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'confirm'): void
    (e: 'cancel'): void
}>()

const close = () => {
    emit('update:modelValue', false)
    emit('cancel')
}

const confirm = () => {
    emit('update:modelValue', false)
    emit('confirm')
}
</script>

<template>
    <Teleport to="body">
        <Transition name="fade">
            <div v-if="modelValue" class="confirm-overlay" @click.self="close">
                <div class="confirm-dialog">
                    <div class="confirm-icon" :class="{ danger }">
                        {{ danger ? '⚠️' : '❓' }}
                    </div>
                    <h3>{{ title || translateLanguage('admin.confirm_dialog.default_title') }}</h3>
                    <p>{{ message || translateLanguage('admin.confirm_dialog.default_message') }}</p>
                    <div class="confirm-actions">
                        <button class="btn btn-outline" @click="close">
                            {{ cancelText || translateLanguage('admin.confirm_dialog.cancel') }}
                        </button>
                        <button 
                            class="btn" 
                            :class="danger ? 'btn-danger' : 'btn-primary'" 
                            @click="confirm"
                        >
                            {{ confirmText || translateLanguage('admin.confirm_dialog.confirm') }}
                        </button>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<style scoped>
.confirm-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.confirm-dialog {
    background: white;
    border-radius: var(--radius-lg);
    padding: 2rem;
    max-width: 400px;
    text-align: center;
    box-shadow: var(--shadow-xl);
}

.confirm-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.confirm-dialog h3 {
    margin-bottom: 0.5rem;
}

.confirm-dialog p {
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}

.confirm-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
}

.btn-danger {
    background: #ef4444;
    color: white;
}

.btn-danger:hover {
    background: #dc2626;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.2s;
}

.fade-enter-from, .fade-leave-to {
    opacity: 0;
}
</style>
