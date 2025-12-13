<script setup lang="ts">
defineProps<{
    type?: 'info' | 'success' | 'warning' | 'error'
    dismissible?: boolean
}>()

const emit = defineEmits<{
    (e: 'dismiss'): void
}>()

const visible = ref(true)

const dismiss = () => {
    visible.value = false
    emit('dismiss')
}
</script>

<template>
    <div v-if="visible" class="alert" :class="`alert-${type || 'info'}`">
        <div class="alert-content">
            <slot />
        </div>
        <button v-if="dismissible" class="dismiss-btn" @click="dismiss">×</button>
    </div>
</template>

<style scoped>
.alert {
    padding: 1rem 1.25rem;
    border-radius: var(--radius);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.alert-info {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #1e40af;
}

.alert-success {
    background: #dcfce7;
    border: 1px solid #86efac;
    color: #166534;
}

.alert-warning {
    background: #fef3c7;
    border: 1px solid #fcd34d;
    color: #92400e;
}

.alert-error {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
}

.dismiss-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    opacity: 0.6;
    transition: opacity 0.2s;
}

.dismiss-btn:hover {
    opacity: 1;
}
</style>
