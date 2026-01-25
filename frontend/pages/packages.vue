<script setup lang="ts">
import { gsap } from 'gsap'

const { translateLanguage } = useLanguage()

useHead({
    title: translateLanguage('packages.title'),
    meta: [
        { name: 'description', content: translateLanguage('packages.meta_desc') }
    ]
})

// Mock Data for Packages
const packages = [
    {
        id: 1,
        name: translateLanguage('packages.pkg1_name'),
        description: translateLanguage('packages.pkg1_desc'),
        price: 12999,
        image: "/images/pkg-bridal.png",
        tags: ["Bridal", "Diamond", "Gold"]
    },
    {
        id: 2,
        name: translateLanguage('packages.pkg2_name'),
        description: translateLanguage('packages.pkg2_desc'),
        price: 5499,
        image: "/images/pkg-anniversary.png",
        tags: ["Anniversary", "Romance"]
    },
    {
        id: 3,
        name: translateLanguage('packages.pkg3_name'),
        description: translateLanguage('packages.pkg3_desc'),
        price: 2899,
        image: "https://images.unsplash.com/photo-1599643478518-17488fbbcd75?q=80&w=1000&auto=format&fit=crop",
        tags: ["Daily", "Minimalist"]
    },
    {
        id: 4,
        name: translateLanguage('packages.pkg4_name'),
        description: translateLanguage('packages.pkg4_desc'),
        price: 25000,
        image: "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?q=80&w=1000&auto=format&fit=crop",
        tags: ["Luxury", "Gemstone"]
    }
]

onMounted(() => {
    gsap.from('.package-card', {
        y: 50,
        opacity: 0,
        stagger: 0.15,
        duration: 0.8,
        ease: 'power2.out'
    })
})
</script>

<template>
    <div class="packages-page">
        <!-- Hero -->
        <section class="page-hero">
            <div class="container">
                <h1>{{ translateLanguage('packages.hero_title') }}</h1>
                <p>{{ translateLanguage('packages.hero_subtitle') }}</p>
            </div>
        </section>

        <!-- Content -->
        <section class="content-section">
            <div class="container">
                <div class="packages-grid">
                    <div v-for="pkg in packages" :key="pkg.id" class="package-card">
                        <div class="card-image">
                            <img :src="pkg.image" :alt="pkg.name" class="package-img">
                            <div class="price-tag">{{ pkg.price.toLocaleString() }} {{ translateLanguage('common.currency') }}</div>
                        </div>
                        <div class="card-content">
                            <div class="tags">
                                <span v-for="tag in pkg.tags" :key="tag" class="tag">{{ tag }}</span>
                            </div>
                            <h3>{{ pkg.name }}</h3>
                            <p>{{ pkg.description }}</p>
                            <button class="btn btn-primary w-100">{{ translateLanguage('packages.view_details') }}</button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Custom Inquiry CTA -->
        <section class="inquiry-section">
            <div class="container">
                <div class="inquiry-box">
                    <h2>{{ translateLanguage('packages.custom_title') }}</h2>
                    <p>{{ translateLanguage('packages.custom_desc') }}</p>
                    <NuxtLink to="/contact" class="btn btn-outline-white">{{ translateLanguage('packages.request') }}</NuxtLink>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.packages-page {
    min-height: 100vh;
}

.page-hero {
    background: var(--surface);
    padding: 5rem 0;
    text-align: center;
    border-bottom: 1px solid var(--border);
}

.page-hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: var(--text);
}

.page-hero p {
    color: var(--text-muted);
    font-size: 1.25rem;
}

.content-section {
    padding: 4rem 0;
}

.packages-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2.5rem;
}

.package-card {
    background: white;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    overflow: hidden;
    transition: all 0.3s;
}

.package-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary);
}

.card-image {
    height: 250px;
    background: #f8fafc;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.package-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.price-tag {
    position: absolute;
    bottom: 1rem;
    right: 1rem;
    background: rgba(255, 255, 255, 0.9);
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    font-weight: 700;
    color: var(--primary);
    box-shadow: var(--shadow);
}

.card-content {
    padding: 2rem;
}

.tags {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.tag {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    background: var(--surface);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
}

.card-content h3 {
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
    color: var(--text);
}

.card-content p {
    color: var(--text-muted);
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

.w-100 {
    width: 100%;
}

.inquiry-section {
    padding: 4rem 0;
    margin-bottom: 4rem;
}

.inquiry-box {
    background: linear-gradient(135deg, var(--primary) 0%, #a855f7 100%);
    padding: 4rem;
    border-radius: var(--radius-lg);
    text-align: center;
    color: white;
}

.inquiry-box h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: white;
}

.inquiry-box p {
    margin-bottom: 2rem;
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.9);
}

.btn-outline-white {
    background: transparent;
    border: 2px solid white;
    color: white;
    padding: 0.75rem 2rem;
    border-radius: var(--radius);
    text-decoration: none;
    font-weight: 600;
    transition: all 0.2s;
}

.btn-outline-white:hover {
    background: white;
    color: var(--primary);
}

@media (max-width: 768px) {
    .packages-grid {
        grid-template-columns: 1fr;
    }
}
</style>
