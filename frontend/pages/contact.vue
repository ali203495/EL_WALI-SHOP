<script setup lang="ts">
import { gsap } from 'gsap'

const { translateLanguage } = useLanguage()

useHead({
    title: translateLanguage('contact.title'),
    meta: [
        { name: 'description', content: translateLanguage('contact.meta_desc') }
    ]
})

const form = reactive({
    name: '',
    email: '',
    subject: '',
    message: ''
})

const isSubmitting = ref(false)
const submitted = ref(false)
const formRef = ref(null)

const handleSubmit = async () => {
    isSubmitting.value = true
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    isSubmitting.value = false
    submitted.value = true
    
    // Animate success message
    nextTick(() => {
        gsap.from('.success-content', {
            scale: 0.8,
            opacity: 0,
            duration: 0.5,
            ease: 'back.out(1.7)'
        })
    })
}

const resetForm = () => {
    form.name = ''
    form.email = ''
    form.subject = ''
    form.message = ''
    submitted.value = false
    
    nextTick(() => {
        animateFormEntrance()
    })
}

const animateFormEntrance = () => {
    gsap.from('.form-group', {
        y: 20,
        opacity: 0,
        stagger: 0.1,
        duration: 0.5,
        ease: 'power2.out'
    })
}

onMounted(() => {
    // Background blobs animation
    gsap.to('.bg-blob', {
        x: '30px',
        y: '30px',
        rotation: 5,
        duration: 6,
        ease: 'sine.inOut',
        yoyo: true,
        repeat: -1,
        stagger: {
            amount: 3,
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
    
    // Contact cards staggering
    gsap.from('.info-card', {
        y: 40,
        opacity: 0,
        duration: 0.6,
        stagger: 0.15,
        delay: 0.3,
        ease: 'back.out(1.2)'
    })

    // Form entrance
    gsap.from('.form-container', {
        x: 50,
        opacity: 0,
        duration: 0.8,
        delay: 0.5,
        ease: 'power2.out'
    })
})
</script>

<template>
    <div class="contact-page">
        <!-- Background Elements -->
        <div class="bg-blob blob-1"></div>
        <div class="bg-blob blob-2"></div>
        <div class="bg-blob blob-3"></div>
        
        <!-- Hero Section -->
        <section class="hero-section">
            <div class="container hero-content">
                <span class="brand-tag">{{ translateLanguage('contact.support') }}</span>
                <h1>{{ translateLanguage('contact.hero_title_1') }} <span class="gradient-text">{{ translateLanguage('contact.hero_title_2') }}</span></h1>
                <p>{{ translateLanguage('contact.hero_subtitle') }}</p>
            </div>
        </section>

        <!-- Main Content -->
        <section class="container content-section">
            <div class="contact-grid">
                <!-- Info Column -->
                <div class="info-column">
                    <div class="info-card glass-panel">
                        <div class="icon-box">📍</div>
                        <div class="card-content">
                            <h3>{{ translateLanguage('contact.visit_flagship') }}</h3>
                            <p>{{ translateLanguage('contact.hq_name') }}<br>{{ translateLanguage('contact.hq_address') }}</p>
                            <a href="https://www.google.com/maps/search/?api=1&query=31.5370,-7.9692" target="_blank" class="card-link">{{ translateLanguage('boutique.get_directions') }} →</a>
                        </div>
                    </div>
                    
                    <div class="info-card glass-panel">
                        <div class="icon-box">📞</div>
                        <div class="card-content">
                            <h3>{{ translateLanguage('contact.call_support') }}</h3>
                            <p class="highlight">+971 4 123 4567</p>
                            <p>Mon-Sat 10:00 - 22:00 (GST)</p>
                        </div>
                    </div>
                    
                    <div class="info-card glass-panel">
                        <div class="icon-box">✉️</div>
                        <div class="card-content">
                            <h3>{{ translateLanguage('contact.email_us') }}</h3>
                            <p class="highlight">concierge@maisonelwali.com</p>
                            <p>24/7 Priority Support</p>
                        </div>
                    </div>

                    <div class="social-links">
                        <a href="#" class="social-btn">𝕏</a>
                        <a href="#" class="social-btn">📷</a>
                        <a href="#" class="social-btn">▶️</a>
                        <a href="#" class="social-btn">💼</a>
                    </div>
                </div>

                <!-- Form Column -->
                <div class="form-column">
                    <div class="glass-container form-container">
                        <div v-if="submitted" class="success-message">
                            <div class="success-content">
                                <div class="success-icon">✨</div>
                                <h2>{{ translateLanguage('contact.message_received') }}</h2>
                                <p>{{ translateLanguage('contact.thanks') }}</p>
                                <button class="btn btn-outline" @click="resetForm">{{ translateLanguage('contact.send_another') }}</button>
                            </div>
                        </div>
                        
                        <form v-else ref="formRef" @submit.prevent="handleSubmit">
                            <h2>{{ translateLanguage('contact.send_message') }}</h2>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label>{{ translateLanguage('contact.name') }}</label>
                                    <input v-model="form.name" type="text" required class="input-field" placeholder="John Doe">
                                </div>
                                <div class="form-group">
                                    <label>{{ translateLanguage('common.email') }}</label>
                                    <input v-model="form.email" type="email" required class="input-field" placeholder="john@example.com">
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label>{{ translateLanguage('contact.subject') }}</label>
                                <select v-model="form.subject" required class="input-field select-field">
                                    <option value="" disabled selected>{{ translateLanguage('contact.topic_placeholder') }}</option>
                                    <option value="sales">{{ translateLanguage('contact.topic_sales') }}</option>
                                    <option value="support">{{ translateLanguage('contact.topic_support') }}</option>
                                    <option value="partnership">{{ translateLanguage('contact.topic_partnership') }}</option>
                                    <option value="other">{{ translateLanguage('contact.topic_other') }}</option>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label>{{ translateLanguage('contact.message') }}</label>
                                <textarea v-model="form.message" rows="5" required class="input-field" :placeholder="translateLanguage('contact.message_placeholder')"></textarea>
                            </div>
                            
                            <button type="submit" class="btn btn-primary btn-block" :disabled="isSubmitting">
                                <span v-if="isSubmitting" class="loading-spinner"></span>
                                {{ isSubmitting ? translateLanguage('contact.sending') : translateLanguage('contact.send_btn') }}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.contact-page {
    position: relative;
    overflow: hidden;
    background: var(--background);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
    position: relative;
    z-index: 1;
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
    top: -100px;
    right: -100px;
}

.blob-2 {
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, #a855f7 0%, transparent 70%);
    bottom: 0;
    left: -100px;
}

.blob-3 {
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, #06b6d4 0%, transparent 70%);
    top: 50%;
    left: 40%;
    opacity: 0.2;
}

/* Glass Styles */
.glass-container {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 2rem;
    padding: 3rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.05);
}

.glass-panel {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.4);
    border-radius: 1.5rem;
    padding: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-panel:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    background: rgba(255, 255, 255, 0.8);
}

/* Hero Section */
.hero-section {
    padding-top: 6rem;
    padding-bottom: 4rem;
    text-align: center;
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
}

/* Content Grid */
.contact-grid {
    display: grid;
    grid-template-columns: 1fr 1.5fr;
    gap: 4rem;
    padding-bottom: 6rem;
}

/* Info Column */
.info-column {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.info-card {
    display: flex;
    gap: 1.5rem;
    align-items: flex-start;
}

.icon-box {
    font-size: 2rem;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 1rem;
}

.card-content h3 {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.card-content p {
    color: var(--text-muted);
    line-height: 1.5;
    font-size: 0.95rem;
}

.highlight {
    color: var(--primary);
    font-weight: 600;
}

.card-link {
    display: inline-block;
    margin-top: 0.5rem;
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
}

.card-link:hover {
    text-decoration: underline;
}

.social-links {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.social-btn {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    text-decoration: none;
    border: 1px solid var(--border);
    transition: all 0.2s;
}

.social-btn:hover {
    background: var(--primary);
    border-color: var(--primary);
    transform: translateY(-3px);
    filter: grayscale(100%) brightness(200%); /* Make emoji whiteish */
}

/* Form Styles */
.form-container h2 {
    margin-bottom: 2rem;
    font-size: 1.75rem;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.input-field {
    width: 100%;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    font-family: inherit;
    font-size: 1rem;
    transition: all 0.3s;
}

.input-field:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px var(--primary-light);
    background: white;
}

.select-field {
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 1rem center;
    background-size: 1em;
}

.btn-block {
    width: 100%;
    padding: 1rem;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.75rem;
}

.loading-spinner {
    width: 1.25rem;
    height: 1.25rem;
    border: 2px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Success State */
.success-message {
    text-align: center;
    padding: 2rem;
}

.success-icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    display: inline-block;
    filter: drop-shadow(0 0 20px rgba(var(--primary-rgb), 0.3));
}

.success-message h2 {
    margin-bottom: 1rem;
}

.success-message p {
    color: var(--text-muted);
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* Responsive */
@media (max-width: 900px) {
    .contact-grid {
        grid-template-columns: 1fr;
        gap: 3rem;
    }
    
    .form-column {
        order: -1; /* Form first on mobile */
    }
}

@media (max-width: 600px) {
    .form-row {
        grid-template-columns: 1fr;
    }
    
    .hero-content h1 {
        font-size: 3rem;
    }
    
    .glass-container {
        padding: 1.5rem;
    }
}
</style>
