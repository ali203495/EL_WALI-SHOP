<script setup lang="ts">
import gsap from 'gsap'

const props = defineProps<{
    modelValue: boolean
    title?: string
    size?: 'sm' | 'md' | 'lg'
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'close'): void
}>()

const modalRef = ref<HTMLElement | null>(null)

const close = () => {
    emit('update:modelValue', false)
    emit('close')
}

watch(() => props.modelValue, (show) => {
    if (show && modalRef.value) {
        gsap.from(modalRef.value.querySelector('.modal-content'), {
            scale: 0.9,
            opacity: 0,
            duration: 0.2,
            ease: 'power2.out'
        })
    }
})
</script>

<template>
    <Teleport to="body">
        <div v-if="modelValue" ref="modalRef" class="modal-overlay" @click.self="close">
            <div class="modal-content" :class="[`modal-${size || 'md'}`]">
                <div class="modal-header" v-if="title">
                    <h3>{{ title }}</h3>
                    <button class="close-btn" @click="close">×</button>
                </div>
                <div class="modal-body">
                    <slot />
                </div>
                <div class="modal-footer" v-if="$slots.footer">
                    <slot name="footer" />
                </div>
            </div>
        </div>
    </Teleport>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 2rem;
}

.modal-content {
    background: var(--surface);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-xl);
    max-height: 90vh;
    overflow-y: auto;
}

.modal-sm { width: 400px; }
.modal-md { width: 560px; }
.modal-lg { width: 800px; }

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid var(--border);
}

.modal-header h3 {
    margin: 0;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--text-muted);
    line-height: 1;
}

.close-btn:hover {
    color: var(--text);
}

.modal-body {
    padding: 1.5rem;
}

.modal-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
}
</style>
