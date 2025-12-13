<script setup lang="ts">
interface Store {
    id: number
    name: string
    address: string
    city: string
    phone: string
    latitude: number
    longitude: number
}

defineProps<{
    store: Store
    selected?: boolean
}>()

defineEmits<{
    (e: 'select', store: Store): void
}>()
</script>

<template>
    <div 
        class="store-card" 
        :class="{ selected }"
        @click="$emit('select', store)"
    >
        <div class="store-header">
            <h4>{{ store.name }}</h4>
            <span class="city-badge">{{ store.city.split(',')[0] }}</span>
        </div>
        
        <p class="store-detail">
            <span class="icon">📍</span>
            {{ store.address }}, {{ store.city }}
        </p>
        
        <p class="store-detail">
            <span class="icon">📞</span>
            {{ store.phone }}
        </p>
        
        <div class="store-actions">
            <a 
                :href="`https://www.google.com/maps/search/?api=1&query=${store.latitude},${store.longitude}`" 
                target="_blank"
                class="btn btn-sm btn-primary"
                @click.stop
            >
                Directions
            </a>
            <a 
                :href="`tel:${store.phone}`" 
                class="btn btn-sm btn-outline"
                @click.stop
            >
                Call
            </a>
        </div>
    </div>
</template>

<style scoped>
.store-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    cursor: pointer;
    transition: all 0.2s;
}

.store-card:hover,
.store-card.selected {
    border-color: var(--primary);
    box-shadow: var(--shadow);
}

.store-card.selected {
    background: var(--primary-light);
}

.store-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.store-header h4 {
    font-size: 1.1rem;
}

.city-badge {
    background: #f1f5f9;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    color: var(--text-muted);
}

.store-detail {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.icon {
    font-size: 1rem;
}

.store-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
}
</style>
