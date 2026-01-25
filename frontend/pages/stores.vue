<script setup lang="ts">
import { gsap } from 'gsap'

const { translateLanguage } = useLanguage()

useHead({
    title: `${translateLanguage('stores.title')} | Maison El Wali`,
    meta: [
        { name: 'description', content: translateLanguage('stores.meta_desc') }
    ]
})

const api = useApi()
const { data: stores, pending: storesLoading, error: storesError, refresh } = await api.getStores()

const handleRetry = () => {
    refresh()
}

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
        <!-- Loading State -->
        <PageLoading v-if="storesLoading" :message="translateLanguage('admin.loading_data')" />

        <!-- Error State -->
        <ErrorState 
            v-else-if="storesError" 
            icon="📍" 
            :title="translateLanguage('admin.failed_load')" 
            :description="translateLanguage('common.error_desc')"
            :retryable="true"
            @retry="handleRetry"
        >
            <template #footer>
                <div class="error-details">
                    {{ storesError.message || storesError.statusText || storesError }}
                </div>
            </template>
        </ErrorState>

        <template v-else>
            <!-- Hero -->
            <section class="stores-hero">
                <div class="container">
                    <h1>{{ translateLanguage('stores.hero_title') }}</h1>
                    <p>{{ translateLanguage('stores.hero_subtitle') }}</p>
                </div>
            </section>

            <!-- Store Locator -->
            <section class="locator-section">
                <div class="container">
                    <div class="locator-layout">
                        <!-- Store List -->
                        <div class="store-list">
                            <h3>{{ stores?.length || 0 }} {{ translateLanguage('stores.locations') }}</h3>
                            
                            <div 
                                v-for="store in stores || []" 
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
                                        {{ translateLanguage('stores.get_directions') }}
                                    </a>
                                    <a :href="`tel:${store.phone}`" class="btn btn-sm btn-outline">
                                        {{ translateLanguage('boutique.call') }}
                                    </a>
                                </div>
                            </div>
                            
                            <div v-if="!stores || stores.length === 0" class="empty-state">
                                <p>{{ translateLanguage('admin.failed_load') }}</p>
                            </div>
                        </div>
                        
                        <!-- Map Area -->
                        <div class="map-area">
                            <img src="/images/luxury-map.png" alt="Maison El Wali Boutique Locations" class="full-map-image animate-fadeIn">
                            
                            <div v-if="selectedStore" class="store-overlay glass-panel">
                                <h4>{{ selectedStore.name }}</h4>
                                <p>{{ selectedStore.address }}, {{ selectedStore.city }}</p>
                                <a :href="`https://www.google.com/maps/search/?api=1&query=${selectedStore.latitude},${selectedStore.longitude}`" target="_blank" class="btn btn-sm btn-primary">
                                    {{ translateLanguage('stores.get_directions') }}
                                </a>
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
                            <h4>{{ translateLanguage('stores.hours') }}</h4>
                            <p>{{ translateLanguage('stores.mon_sat') }}: 10AM - 9PM<br>{{ translateLanguage('stores.sun') }}: 11AM - 7PM</p>
                        </div>
                        <div class="info-card">
                            <span class="info-icon">👨‍💼</span>
                            <h4>{{ translateLanguage('stores.expert_staff') }}</h4>
                            <p>{{ translateLanguage('stores.expert_desc') }}</p>
                        </div>
                        <div class="info-card">
                            <span class="info-icon">🔧</span>
                            <h4>{{ translateLanguage('stores.service_center') }}</h4>
                            <p>{{ translateLanguage('stores.service_desc') }}</p>
                        </div>
                    </div>
                </div>
            </section>
        </template>
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
    position: relative;
    background: #e2e8f0;
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.full-map-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.store-overlay {
    position: absolute;
    bottom: 2rem;
    left: 2rem;
    right: 2rem;
    padding: 1.5rem;
    max-width: 320px;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid var(--primary);
    box-shadow: var(--shadow-xl);
}

.store-overlay h4 {
    margin-bottom: 0.5rem;
    color: var(--text);
}

.store-overlay p {
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
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
