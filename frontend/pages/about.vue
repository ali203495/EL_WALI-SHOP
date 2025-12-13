<script setup lang="ts">
import gsap from 'gsap'

onMounted(() => {
    // Background blobs animation
    gsap.to('.bg-blob', {
        y: '50px',
        rotation: 10,
        duration: 5,
        ease: 'sine.inOut',
        yoyo: true,
        repeat: -1,
        stagger: {
            amount: 2,
            from: "random"
        }
    })

    // Hero content entrance
    const tl = gsap.timeline()
    tl.from('.hero-content h1', {
        y: 50,
        opacity: 0,
        duration: 1,
        ease: 'power3.out'
    })
    .from('.hero-content p', {
        y: 30,
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out'
    }, '-=0.6')
    
    // Mission section entrance
    gsap.from('.mission-card', {
        scrollTrigger: {
            trigger: '.mission-section',
            start: 'top 80%',
        },
        y: 50,
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out'
    })

    // Values staggering
    gsap.from('.value-card', {
        scrollTrigger: {
            trigger: '.values-grid',
            start: 'top 80%',
        },
        y: 40,
        opacity: 0,
        duration: 0.6,
        stagger: 0.2,
        ease: 'back.out(1.2)'
    })
})

useHead({
    title: 'About Us | LUXE.TECH',
    meta: [
        { name: 'description', content: 'Experience the future of technology at LUXE.TECH. Premium devices, curated selection, and expert guidance.' }
    ]
})
</script>

<template>
    <div class="about-page">
        <!-- Background Elements -->
        <div class="bg-blob blob-1"></div>
        <div class="bg-blob blob-2"></div>
        
        <!-- Hero Section -->
        <section class="hero-section">
            <div class="glass-container hero-container">
                <div class="hero-content">
                    <span class="brand-tag">LUXE.TECH</span>
                    <h1>Curating the<br><span class="gradient-text">Future of Tech</span></h1>
                    <p>Your premier destination for premium devices and cutting-edge innovations.</p>
                </div>
            </div>
        </section>

        <!-- Mission Section -->
        <section class="mission-section container">
            <div class="mission-card glass-panel">
                <div class="mission-content">
                    <h2>Our Mission</h2>
                    <p class="mission-text">
                        We believe technology should be more than just functional—it should be an experience. 
                        At LUXE.TECH, we bridge the gap between premium design and human potential.
                    </p>
                    <div class="stats-row">
                        <div class="stat-item">
                            <span class="stat-number">50+</span>
                            <span class="stat-label">Premium Brands</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">12</span>
                            <span class="stat-label">Global Showrooms</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">24/7</span>
                            <span class="stat-label">Expert Support</span>
                        </div>
                    </div>
                </div>
                <div class="mission-visual">
                    <div class="visual-circle"></div>
                    <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80" alt="Futuristic Architecture" class="mission-img">
                </div>
            </div>
        </section>

        <!-- Values Section -->
        <section class="values-section container">
            <div class="section-header">
                <h2>Why Choose Us</h2>
                <p>The standards that define our collection</p>
            </div>
            <div class="values-grid">
                <div class="value-card glass-panel">
                    <div class="icon-box">💎</div>
                    <h3>Curated Excellence</h3>
                    <p>Every product is hand-picked for superior build quality, design, and performance.</p>
                </div>
                <div class="value-card glass-panel">
                    <div class="icon-box">🚀</div>
                    <h3>Innovation First</h3>
                    <p>Access the latest technology as soon as it launches, ahead of the mass market.</p>
                </div>
                <div class="value-card glass-panel">
                    <div class="icon-box">🛡️</div>
                    <h3>Premium Guarantee</h3>
                    <p>Comprehensive warranty coverage and dedicated concierge support for every purchase.</p>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="cta-section">
            <div class="glass-container cta-container">
                <h2>Ready to Experience It?</h2>
                <p>Visit our digital showroom or find a location near you.</p>
                <div class="cta-actions">
                    <NuxtLink to="/catalog" class="btn btn-primary btn-lg">Browse Collection</NuxtLink>
                    <NuxtLink to="/stores" class="btn btn-outline btn-lg">Find a Store</NuxtLink>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.about-page {
    position: relative;
    overflow: hidden;
    background: var(--background);
    min-height: 100vh;
}

/* Common Glass Styles */
.glass-container {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.5);
}

.glass-panel {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    border-radius: 1.5rem;
}

/* Background Blobs */
.bg-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    z-index: 0;
    opacity: 0.4;
    pointer-events: none;
}

.blob-1 {
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
    top: -200px;
    right: -100px;
}

.blob-2 {
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, #06b6d4 0%, transparent 70%);
    bottom: -100px;
    left: -100px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
    position: relative;
    z-index: 1;
}

/* Hero Section */
.hero-section {
    padding-top: 4rem;
    padding-bottom: 6rem;
    text-align: center;
    position: relative;
    z-index: 1;
}

.hero-container {
    padding: 6rem 1.5rem;
    margin: 0 1.5rem;
    border-radius: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.5);
}

.brand-tag {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: rgba(0, 0, 0, 0.05);
    border-radius: 2rem;
    font-size: 0.875rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 1.5rem;
    letter-spacing: 0.1em;
}

.hero-content h1 {
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    color: var(--text);
}

.gradient-text {
    background: linear-gradient(135deg, var(--primary) 0%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-content p {
    font-size: 1.25rem;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Mission Section */
.mission-section {
    margin-bottom: 6rem;
}

.mission-card {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    padding: 4rem;
    overflow: hidden;
}

.mission-content h2 {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
}

.mission-text {
    font-size: 1.125rem;
    line-height: 1.7;
    color: var(--text-muted);
    margin-bottom: 3rem;
}

.stats-row {
    display: flex;
    gap: 3rem;
}

.stat-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.stat-number {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text);
}

.stat-label {
    font-size: 0.875rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.mission-visual {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.mission-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 1rem;
    position: relative;
    z-index: 2;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    transform: rotate(2deg);
    transition: transform 0.5s ease;
}

.mission-card:hover .mission-img {
    transform: rotate(0deg) scale(1.02);
}

.visual-circle {
    position: absolute;
    width: 80%;
    height: 80%;
    border: 2px solid var(--primary);
    border-radius: 50%;
    opacity: 0.1;
    z-index: 1;
    transform: translate(-10%, -10%);
}

/* Values Section */
.values-section {
    margin-bottom: 8rem;
}

.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-header h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.section-header p {
    color: var(--text-muted);
    font-size: 1.125rem;
}

.values-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
}

.value-card {
    padding: 2.5rem;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.value-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.05);
    border-color: var(--primary);
}

.icon-box {
    font-size: 3rem;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    margin-left: auto;
    margin-right: auto;
}

.value-card h3 {
    font-size: 1.25rem;
    margin-bottom: 1rem;
}

.value-card p {
    color: var(--text-muted);
    line-height: 1.6;
}

/* CTA Section */
.cta-section {
    padding: 0 1.5rem 6rem;
    text-align: center;
}

.cta-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 5rem 2rem;
    border-radius: 2rem;
}

.cta-container h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.cta-container p {
    font-size: 1.25rem;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
}

.cta-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
}

/* Responsive */
@media (max-width: 1024px) {
    .mission-card {
        grid-template-columns: 1fr;
        padding: 3rem;
        gap: 3rem;
    }

    .mission-img {
        height: 300px;
    }
}

@media (max-width: 768px) {
    .hero-content h1 {
        font-size: 2.5rem;
    }

    .values-grid {
        grid-template-columns: 1fr;
    }

    .cta-actions {
        flex-direction: column;
    }
}
</style>
