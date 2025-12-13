<script setup lang="ts">
const isOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const toggle = () => {
    isOpen.value = !isOpen.value
}

const close = () => {
    isOpen.value = false
}

// Close on click outside
onMounted(() => {
    document.addEventListener('click', (e) => {
        if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) {
            close()
        }
    })
})
</script>

<template>
    <div ref="dropdownRef" class="dropdown" :class="{ open: isOpen }">
        <div class="dropdown-trigger" @click="toggle">
            <slot name="trigger" />
        </div>
        <div v-if="isOpen" class="dropdown-menu">
            <slot @click="close" />
        </div>
    </div>
</template>

<style scoped>
.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown-trigger {
    cursor: pointer;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    margin-top: 0.5rem;
    background: white;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    min-width: 180px;
    z-index: 100;
    animation: dropIn 0.15s ease;
}

@keyframes dropIn {
    from {
        opacity: 0;
        transform: translateY(-8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.dropdown-menu :deep(a),
.dropdown-menu :deep(button) {
    display: block;
    width: 100%;
    padding: 0.75rem 1rem;
    text-align: left;
    background: none;
    border: none;
    font-size: 0.875rem;
    color: var(--text);
    text-decoration: none;
    cursor: pointer;
}

.dropdown-menu :deep(a:hover),
.dropdown-menu :deep(button:hover) {
    background: #f8fafc;
}
</style>
