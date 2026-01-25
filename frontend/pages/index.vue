<script setup lang="ts">
import { gsap } from 'gsap'
import { useLanguage } from '../composables/useLanguage'

const { translateLanguage } = useLanguage()

useHead({
    title: translateLanguage('home.title'),
    meta: [
        { name: 'description', content: translateLanguage('home.meta_desc') }
    ]
})

const { settings } = useSiteSettings()

onMounted(() => {
    const tl = gsap.timeline()
    
    tl.from('.hero-content > *', {
        y: 50,
        opacity: 0,
        duration: 1,
        stagger: 0.2,
        ease: 'power3.out'
    })
    
    tl.from('.value-prop', {
        y: 30,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: 'power2.out'
    }, '-=0.5')
})
</script>

<template>
    <div class="home-page">
        <!-- Hero Section -->
        <section class="hero-section">
            <div class="hero-bg">
                <div class="gradient-orb orb-1"></div>
                <div class="gradient-orb orb-2"></div>
            </div>
            
            <div class="container hero-content">
                <span class="eyebrow">{{ settings.hero_badge }}</span>
                <h1>{{ settings.hero_title }}</h1>
                <p class="subtitle">{{ settings.hero_subtitle }}</p>
                
                <div class="hero-actions">
                    <NuxtLink to="/catalog" class="btn btn-primary btn-lg">{{ translateLanguage('common.explore') }}</NuxtLink>
                    <NuxtLink to="/boutique" class="btn btn-outline btn-lg text-white">{{ translateLanguage('common.visit') }}</NuxtLink>
                </div>
            </div>
        </section>

        <!-- Value Props -->
        <section class="values-section">
            <div class="container">
                <div class="values-grid">
                    <div class="value-prop">
                        <span class="icon">✨</span>
                        <h3>{{ translateLanguage('home.luxury_authentic') }}</h3>
                        <p>{{ translateLanguage('home.luxury_desc') }}</p>
                    </div>
                    <div class="value-prop">
                        <span class="icon">🌍</span>
                        <h3>{{ translateLanguage('home.global_shipping') }}</h3>
                        <p>{{ translateLanguage('home.shipping_desc') }}</p>
                    </div>
                    <div class="value-prop">
                        <span class="icon">💎</span>
                        <h3>{{ translateLanguage('home.bespoke_design') }}</h3>
                        <p>{{ translateLanguage('home.bespoke_desc') }}</p>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Featured Teaser -->
        <section class="teaser-section">
             <div class="container teaser-content">
                <div class="teaser-text">
                    <h2>{{ translateLanguage('home.gold_standard') }}</h2>
                    <p>{{ translateLanguage('home.teaser_desc') }}</p>
                    <NuxtLink to="/about" class="link-arrow">{{ translateLanguage('home.read_story') }} →</NuxtLink>
                </div>
                <!-- Decorative Image Placeholder -->
                <div class="teaser-visual">
                    <img src="/images/jewelry-teaser.png" alt="Maison El Wali Luxury Jewelry" class="teaser-image animate-fadeInUp">
                </div>
             </div>
        </section>
    </div>
</template>

<style scoped>
.home-page {
    min-height: 100vh;
    background: #0f172a;
    color: white;
}

/* Hero */
.hero-section {
    min-height: 90vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    text-align: center;
    padding-top: 60px; /* Navbar offset */
}

.hero-bg {
    position: absolute;
    inset: 0;
    z-index: 0;
}

.gradient-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px); /* Reduced blur for performance */
    opacity: 0.4;
}

.orb-1 {
    width: 60vh;
    height: 60vh;
    background: linear-gradient(135deg, var(--primary) 0%, #7c3aed 100%);
    top: -10vh;
    left: -10vw;
}

.orb-2 {
    width: 50vh;
    height: 50vh;
    background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
    bottom: -10vh;
    right: -10vw;
}

.hero-content {
    position: relative;
    z-index: 10;
    max-width: 800px;
    padding: 0 2rem;
}

.eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.3em;
    font-size: 0.875rem;
    color: var(--primary);
    margin-bottom: 1.5rem;
    display: block;
    font-weight: 600;
}

h1 {
    font-size: 5rem;
    line-height: 1.1;
    font-weight: 800;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}

.text-gradient {
    background: linear-gradient(to right, #fff, #cbd5e1);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-size: 1.25rem;
    color: #94a3b8;
    margin-bottom: 3rem;
    line-height: 1.6;
}

.hero-actions {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    flex-wrap: wrap;
}

.text-white {
    color: white !important;
    border-color: rgba(255,255,255,0.2) !important;
}

.text-white:hover {
    background: rgba(255,255,255,0.05) !important;
    border-color: white !important;
}

/* Values */
.values-section {
    padding: 6rem 0;
    background: rgba(15, 23, 42, 0.8);
    border-top: 1px solid rgba(255,255,255,0.05);
}

.values-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 3rem;
}

.value-prop {
    text-align: center;
    padding: 2rem;
    background: rgba(255,255,255,0.03);
    border-radius: 1rem;
    transition: transform 0.3s;
}

.value-prop:hover {
    transform: translateY(-5px);
    background: rgba(255,255,255,0.05);
}

.icon {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    display: block;
}

.value-prop h3 {
    font-size: 1.25rem;
    margin-bottom: 1rem;
    color: white;
}

.value-prop p {
    color: #94a3b8;
    line-height: 1.6;
}

/* Teaser */
.teaser-section {
    padding: 6rem 0;
    background: white;
    color: var(--text);
}

.teaser-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
}

.teaser-text h2 {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    color: var(--text);
}

.teaser-text p {
    font-size: 1.125rem;
    color: var(--text-muted);
    margin-bottom: 2rem;
    line-height: 1.7;
}

.link-arrow {
    color: var(--primary);
    text-decoration: none;
    font-weight: 600;
    font-size: 1.125rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: gap 0.2s;
}

.link-arrow:hover {
    gap: 0.75rem;
}

.teaser-visual {
    height: 400px;
    background: #f1f5f9;
    border-radius: 1rem;
    overflow: hidden;
}

.teaser-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.teaser-image:hover {
    transform: scale(1.05);
}

@media (max-width: 768px) {
    h1 {
        font-size: 3rem;
    }
    
    .hero-content {
        padding: 0 1.5rem;
    }
    
    .teaser-content {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
    
    .teaser-visual {
        height: 300px;
        order: -1;
    }
}
</style>
