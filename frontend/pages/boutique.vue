<script setup lang="ts">
import gsap from 'gsap'

useHead({
    title: 'Flagship Boutique',
    meta: [
        { name: 'description', content: 'Visit our flagship boutique in Dubai. Experience luxury service and exclusive jewelry collections.' }
    ]
})

// Mock Boutique Data - singular focus
const boutique = {
    name: "MAISON EL WALI Flagship",
    address: "12 Royal Palm Avenue, Downtown Dubai",
    city: "Dubai, UAE",
    phone: "+971 4 123 4567",
    email: "boutique@maisonelwali.com",
    hours: {
        weekdays: "10:00 AM - 10:00 PM",
        weekends: "10:00 AM - 12:00 AM"
    },
    images: [
        "/images/boutique-interior.jpg",
        "/images/boutique-exterior.jpg"
    ],
    coords: { lat: 25.1972, lng: 55.2744 }
}

onMounted(() => {
    const tl = gsap.timeline()
    
    tl.from('.boutique-hero-content', { 
        y: 50, 
        opacity: 0, 
        duration: 1, 
        ease: 'power3.out' 
    })
    .from('.info-block', {
        y: 30,
        opacity: 0,
        stagger: 0.2,
        duration: 0.8
    }, '-=0.5')
})
</script>

<template>
    <div class="boutique-page">
        <!-- Hero Section -->
        <section class="boutique-hero">
            <div class="hero-bg"></div>
            <div class="container boutique-hero-content">
                <span class="eyebrow">The Experience</span>
                <h1>Our Flagship Boutique</h1>
                <p>Immerse yourself in a world of refined luxury at our Dubai showroom.</p>
            </div>
        </section>

        <!-- Main Content Split -->
        <section class="boutique-details">
            <div class="container">
                <div class="details-grid">
                    <!-- Left: Info -->
                    <div class="info-column">
                        <div class="info-block">
                            <h3>Visit Us</h3>
                            <address>
                                <strong>{{ boutique.name }}</strong><br>
                                {{ boutique.address }}<br>
                                {{ boutique.city }}
                            </address>
                            <div class="contact-actions">
                                <a :href="`https://www.google.com/maps/search/?api=1&query=${boutique.coords.lat},${boutique.coords.lng}`" target="_blank" class="btn btn-primary">
                                    Get Directions
                                </a>
                                <a :href="`tel:${boutique.phone}`" class="btn btn-outline">
                                    Call Boutique
                                </a>
                            </div>
                        </div>

                        <div class="info-block">
                            <h3>Opening Hours</h3>
                            <ul class="hours-list">
                                <li>
                                    <span>Mon - Fri</span>
                                    <span>{{ boutique.hours.weekdays }}</span>
                                </li>
                                <li>
                                    <span>Sat - Sun</span>
                                    <span>{{ boutique.hours.weekends }}</span>
                                </li>
                            </ul>
                        </div>

                        <div class="info-block">
                            <h3>Private Appointments</h3>
                            <p>For a personalized experience, book a private viewing with our senior jewelry consultants.</p>
                            <NuxtLink to="/contact" class="book-link">Book an Appointment →</NuxtLink>
                        </div>
                    </div>

                    <!-- Right: Visual/Map -->
                    <div class="visual-column">
                        <div class="image-showcase">
                            <div class="placeholder-image main-image">
                                <span>Maison Interior</span>
                            </div>
                            <!-- <img src="..." alt="Boutique Interior"> -->
                        </div>
                        <div class="map-preview">
                            <div class="map-placeholder">
                                <span>📍 Map View</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Services -->
        <section class="services-section">
            <div class="container">
                <h2 class="text-center">Boutique Services</h2>
                <div class="services-grid">
                    <div class="service-card">
                        <span class="icon">💎</span>
                        <h4>Custom Design</h4>
                        <p>Work with our artisans to create a one-of-a-kind piece.</p>
                    </div>
                    <div class="service-card">
                        <span class="icon">✨</span>
                        <h4>Jewelry Spa</h4>
                        <p>Professional cleaning and restoration for your precious items.</p>
                    </div>
                    <div class="service-card">
                        <span class="icon">🥂</span>
                        <h4>VIP Lounge</h4>
                        <p>Enjoy refreshments in our private viewing suites.</p>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.boutique-page {
    min-height: 100vh;
}

.boutique-hero {
    height: 60vh;
    background: #0f172a; /* Fallback */
    position: relative;
    display: flex;
    align-items: center;
    color: white;
    text-align: center;
    overflow: hidden;
}

.hero-bg {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 1) 100%);
    z-index: 1;
}

.boutique-hero-content {
    position: relative;
    z-index: 10;
}

.eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.2em;
    font-size: 0.875rem;
    color: var(--primary);
    margin-bottom: 1rem;
    display: block;
}

.boutique-hero h1 {
    font-size: 4rem;
    font-weight: 300;
    margin-bottom: 1.5rem;
}

.boutique-hero p {
    font-size: 1.25rem;
    color: #cbd5e1;
    max-width: 600px;
    margin: 0 auto;
}

/* Details Split */
.boutique-details {
    padding: 6rem 0;
    background: var(--background);
}

.details-grid {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    gap: 5rem;
    align-items: start;
}

.info-block {
    margin-bottom: 3rem;
}

.info-block h3 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    display: inline-block;
}

.info-block h3::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 40px;
    height: 2px;
    background: var(--primary);
}

.info-block address {
    font-style: normal;
    color: var(--text-muted);
    line-height: 1.8;
    margin-bottom: 1.5rem;
}

.contact-actions {
    display: flex;
    gap: 1rem;
}

.hours-list {
    list-style: none;
    color: var(--text-muted);
}

.hours-list li {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--border);
}

.book-link {
    display: inline-block;
    color: var(--primary);
    text-decoration: none;
    font-weight: 600;
    margin-top: 0.5rem;
    transition: transform 0.2s;
}

.book-link:hover {
    transform: translateX(5px);
}

/* Visual Column */
.visual-column {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.image-showcase {
    height: 400px;
    background: #f1f5f9;
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.placeholder-image {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #e2e8f0;
    color: #64748b;
    font-size: 1.5rem;
}

.map-preview {
    height: 200px;
    background: #f1f5f9;
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.map-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #e2e8f0;
    color: #64748b;
}

/* Services */
.services-section {
    padding: 6rem 0;
    background: var(--surface);
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin-top: 4rem;
}

.service-card {
    text-align: center;
    padding: 2rem;
    background: var(--background);
    border-radius: var(--radius-lg);
    border: 1px solid transparent;
    transition: all 0.3s;
}

.service-card:hover {
    border-color: var(--primary);
    transform: translateY(-5px);
    box-shadow: var(--shadow);
}

.service-card .icon {
    font-size: 2.5rem;
    display: block;
    margin-bottom: 1.5rem;
}

.service-card h4 {
    margin-bottom: 1rem;
    font-size: 1.2rem;
}

.service-card p {
    color: var(--text-muted);
}

@media (max-width: 1024px) {
    .details-grid {
        grid-template-columns: 1fr;
        gap: 3rem;
    }
    
    .boutique-hero h1 {
        font-size: 3rem;
    }
}

@media (max-width: 640px) {
    .services-grid {
        grid-template-columns: 1fr;
    }
}
</style>
