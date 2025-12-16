<script setup lang="ts">
const props = defineProps<{
    src?: string
    alt?: string
    name?: string
    size?: 'sm' | 'md' | 'lg' | 'xl'
}>()

const initials = computed(() => {
    if (!props.name) return '?'
    const parts = props.name.split(' ')
    if (parts.length >= 2) {
        return (parts[0]?.[0] || '') + (parts[1]?.[0] || '')
    }
    return props.name.slice(0, 2)
})

const showFallback = ref(false)

const handleError = () => {
    showFallback.value = true
}
</script>

<template>
    <div class="avatar" :class="[`avatar-${size || 'md'}`]">
        <img 
            v-if="src && !showFallback" 
            :src="src" 
            :alt="alt || name" 
            @error="handleError"
        />
        <span v-else class="avatar-fallback">{{ initials.toUpperCase() }}</span>
    </div>
</template>

<style scoped>
.avatar {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: var(--primary-light);
    color: var(--primary);
    font-weight: 700;
    overflow: hidden;
}

.avatar-sm { width: 32px; height: 32px; font-size: 0.75rem; }
.avatar-md { width: 40px; height: 40px; font-size: 0.875rem; }
.avatar-lg { width: 56px; height: 56px; font-size: 1rem; }
.avatar-xl { width: 80px; height: 80px; font-size: 1.5rem; }

.avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-fallback {
    line-height: 1;
}
</style>
