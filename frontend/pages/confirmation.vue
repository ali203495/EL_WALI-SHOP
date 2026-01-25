<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { gsap } from 'gsap'

const { translateLanguage } = useLanguage()
const route = useRoute()
const orderId = route.query.orderId || 'Unknown'
// ... rest of script ...

onMounted(() => {
    // Initial entrance
    gsap.from('.icon-wrapper', {
        scale: 0,
        rotation: -180,
        duration: 0.8,
        ease: 'back.out(1.7)'
    })

    gsap.from('.content > *', {
        y: 20,
        opacity: 0,
        stagger: 0.1,
        duration: 0.6,
        delay: 0.3
    })

    // Confetti effect (simple CSS/JS implementation)
    createConfetti()
})

const createConfetti = () => {
    const colors = ['#4f46e5', '#ec4899', '#10b981', '#f59e0b']
    
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div')
        confetti.classList.add('confetti')
        confetti.style.left = Math.random() * 100 + 'vw'
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)] || '#f59e0b' || '#f59e0b'
        confetti.style.animationDuration = Math.random() * 3 + 2 + 's'
        confetti.style.opacity = Math.random().toString()
        document.body.appendChild(confetti)

        // Remove after animation
        setTimeout(() => {
            confetti.remove()
        }, 5000)
    }
}
</script>

<template>
    <div class="confirmation-page">
        <div class="card">
            <div class="icon-wrapper maison-primary">
                <span class="check-icon">✓</span>
            </div>
            
            <div class="content">
                <h1>{{ translateLanguage('confirmation.title') }}</h1>
                <p class="subtitle">{{ translateLanguage('confirmation.subtitle') }}</p>
                
                <div class="order-details">
                    <p>{{ translateLanguage('confirmation.order_id') }}</p>
                    <span class="order-id">#{{ orderId }}</span>
                </div>
                
                <p class="message">
                    {{ translateLanguage('confirmation.message') }}
                </p>

                <div class="actions">
                    <NuxtLink to="/catalog" class="btn btn-primary btn-lg">
                        {{ translateLanguage('confirmation.continue_shopping') }}
                    </NuxtLink>
                    <NuxtLink to="/" class="btn btn-text">
                        {{ translateLanguage('confirmation.back_home') }}
                    </NuxtLink>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
/* Global confetti styles */
.confetti {
    position: fixed;
    top: -10px;
    width: 10px;
    height: 10px;
    z-index: 9999;
    pointer-events: none;
    animation: fall linear forwards;
}

@keyframes fall {
    to {
        transform: translateY(100vh) rotate(720deg);
    }
}
</style>

<style scoped>
.confirmation-page {
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background: #f8fafc;
    overflow: hidden;
}

.card {
    background: white;
    padding: 3rem 2rem;
    border-radius: var(--radius-lg);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    text-align: center;
    max-width: 500px;
    width: 100%;
    position: relative;
    border: 1px solid var(--border);
}

.icon-wrapper {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 2rem;
    box-shadow: 0 10px 15px -3px rgba(22, 163, 74, 0.3);
}

.check-icon {
    font-size: 3rem;
    color: white;
    font-weight: 800;
}

h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.subtitle {
    font-size: 1.125rem;
    color: var(--text-muted);
    margin-bottom: 2rem;
}

.order-details {
    background: #f1f5f9;
    padding: 1rem;
    border-radius: var(--radius);
    display: inline-block;
    margin-bottom: 2rem;
    min-width: 200px;
}

.order-details p {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
}

.order-id {
    font-family: monospace;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
}

.message {
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 3rem;
}

.actions {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.btn-lg {
    padding: 1rem 2rem;
    font-size: 1.1rem;
}

.btn-text {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.9rem;
}

.btn-text:hover {
    color: var(--text);
}
</style>
