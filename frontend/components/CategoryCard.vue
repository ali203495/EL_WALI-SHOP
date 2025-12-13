<script setup lang="ts">
interface Category {
    id: number
    name: string
    image_url?: string
}

defineProps<{
    category: Category
}>()

// Map category names to icons
const getIcon = (name: string): string => {
    const icons: Record<string, string> = {
        'Laptops': '💻',
        'Smartphones': '📱',
        'Audio': '🎧',
        'TVs & Displays': '📺',
        'Wearables': '⌚',
        'Gaming': '🎮',
        'Cameras': '📷',
    }
    return icons[name] || '📦'
}
</script>

<template>
    <NuxtLink to="/catalog" class="category-card">
        <span class="category-icon">{{ getIcon(category.name) }}</span>
        <h3>{{ category.name }}</h3>
    </NuxtLink>
</template>

<style scoped>
.category-card {
    background: #f8fafc;
    border-radius: var(--radius-lg);
    padding: 2rem;
    text-align: center;
    text-decoration: none;
    color: var(--text);
    transition: all 0.3s;
    border: 2px solid transparent;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.category-card:hover {
    background: white;
    border-color: var(--primary);
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.category-icon {
    font-size: 3rem;
}

.category-card h3 {
    font-size: 1rem;
    font-weight: 600;
}
</style>
