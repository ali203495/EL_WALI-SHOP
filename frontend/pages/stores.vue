<script setup lang="ts">
import gsap from 'gsap'

useHead({
    title: 'Our Locations',
    meta: [
        { name: 'description', content: 'Find a LUXE.TECH premium showroom near you. Experience our products in person.' }
    ]
})

const api = useApi()
const { data: stores } = await api.getStores()

const selectedStore = ref<any>(null)

const selectStore = (store: any) => {
    selectedStore.value = store
}

onMounted(() => {
    gsap.from('.store-card', {
        y: 40,
        opacity: 0,
        stagger: 0.1,
        duration: 0.6,
        ease: 'power2.out'
    })
})
</script>

<template>
    <div class="stores-page">
        <!-- Hero -->
        <section class="stores-hero">
            <div class="container">
                <h1>Find Your Nearest Store</h1>
                <p>Experience our products in person at one of our premium showrooms</p>
            </div>
        </section>

        <!-- Store Locator -->
        <section class="locator-section">
            <div class="container">
                <div class="locator-layout">
                    <!-- Store List -->
                    <div class="store-list">
                        <h3>{{ stores?.length }} Locations</h3>
                        
                        <div 
                            v-for="store in stores" 
                            :key="store.id" 
                            class="store-card"
                            :class="{ active: selectedStore?.id === store.id }"
                            @click="selectStore(store)"
                        >
                            <div class="store-header">
                                <h4>{{ store.name }}</h4>
                                <span class="city-badge">{{ store.city.split(',')[0] }}</span>
                            </div>
                            <p class="store-address">
                                <span class="icon">📍</span>
                                {{ store.address }}, {{ store.city }}
                            </p>
                            <p class="store-phone">
                                <span class="icon">📞</span>
                                {{ store.phone }}
                            </p>
                            <div class="store-actions">
                                <a 
                                    :href="`https://www.google.com/maps/search/?api=1&query=${store.latitude},${store.longitude}`" 
                                    target="_blank"
                                    class="btn btn-sm btn-primary"
                                >
                                    Get Directions
                                </a>
                                <a :href="`tel:${store.phone}`" class="btn btn-sm btn-outline">
                                    Call Store
                                </a>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Map Area -->
                    <div class="map-area">
                        <div class="map-placeholder">
                            <div class="map-content">
                                <span class="map-icon">🗺️</span>
                                <h3>Interactive Map</h3>
                                <p>Connect Google Maps API to display locations</p>
                                
                                <!-- Store Preview -->
                                <div v-if="selectedStore" class="selected-store-preview">
                                    <h4>{{ selectedStore.name }}</h4>
                                    <p>{{ selectedStore.address }}, {{ selectedStore.city }}</p>
                                    <p class="coords">
                                        Lat: {{ selectedStore.latitude.toFixed(4) }}, 
                                        Lng: {{ selectedStore.longitude.toFixed(4) }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Info Section -->
        <section class="info-section">
            <div class="container">
                <div class="info-grid">
                    <div class="info-card">
                        <span class="info-icon">🕐</span>
                        <h4>Store Hours</h4>
                        <p>Mon-Sat: 10AM - 9PM<br>Sun: 11AM - 7PM</p>
                    </div>
                    <div class="info-card">
                        <span class="info-icon">👨‍💼</span>
                        <h4>Expert Staff</h4>
                        <p>Our trained specialists will help you find the perfect device</p>
                    </div>
                    <div class="info-card">
                        <span class="info-icon">🔧</span>
                        <h4>Service Center</h4>
                        <p>In-store repairs and technical support available</p>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.stores-page {
    min-height: 100vh;
}

/* Hero */
.stores-hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 6rem 0;
    text-align: center;
}

.stores-hero h1 {
    color: white;
    font-size: 3rem;
    margin-bottom: 1rem;
}

.stores-hero p {
    color: #94a3b8;
    font-size: 1.25rem;
}

/* Locator */
.locator-section {
    padding: 4rem 0;
}

.locator-layout {
    display: grid;
    grid-template-columns: 400px 1fr;
    gap: 2rem;
    min-height: 600px;
}

.store-list h3 {
    margin-bottom: 1.5rem;
    color: var(--text-muted);
}

.store-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin-bottom: 1rem;
    cursor: pointer;
    transition: all 0.2s;
}

.store-card:hover,
.store-card.active {
    border-color: var(--primary);
    box-shadow: var(--shadow);
}

.store-card.active {
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

.store-address,
.store-phone {
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

/* Map */
.map-area {
    background: #e2e8f0;
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.map-placeholder {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.map-content {
    text-align: center;
    color: #64748b;
}

.map-icon {
    font-size: 4rem;
    display: block;
    margin-bottom: 1rem;
}

.selected-store-preview {
    margin-top: 2rem;
    padding: 1.5rem;
    background: white;
    border-radius: var(--radius);
    text-align: left;
}

.selected-store-preview h4 {
    color: var(--text);
    margin-bottom: 0.5rem;
}

.coords {
    font-size: 0.75rem;
    font-family: monospace;
    margin-top: 0.5rem;
}

/* Info Section */
.info-section {
    padding: 4rem 0;
    background: #f8fafc;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
}

.info-card {
    background: white;
    padding: 2rem;
    border-radius: var(--radius-lg);
    text-align: center;
}

.info-icon {
    font-size: 2.5rem;
    display: block;
    margin-bottom: 1rem;
}

.info-card h4 {
    margin-bottom: 0.5rem;
}

.info-card p {
    color: var(--text-muted);
    font-size: 0.9rem;
}

@media (max-width: 1024px) {
    .locator-layout {
        grid-template-columns: 1fr;
    }
    
    .info-grid {
        grid-template-columns: 1fr;
    }
}
</style>
