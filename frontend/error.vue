<script setup lang="ts">
import { gsap } from 'gsap'

const { translateLanguage } = useLanguage()

onMounted(() => {
    // Initial entrance animations
    const tl = gsap.timeline()

    tl.from('.error-code', {
        y: 50,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out'
    })
    .from('.error-title', {
        y: 30,
        opacity: 0,
        duration: 0.6,
        ease: 'power2.out'
    }, '-=0.4')
    .from('.error-desc', {
        y: 20,
        opacity: 0,
        duration: 0.6,
        ease: 'power2.out'
    }, '-=0.4')
    .from('.action-btn', {
        y: 20,
        opacity: 0,
        duration: 0.5,
        stagger: 0.1,
        ease: 'back.out(1.7)'
    }, '-=0.2')

    // Floating background elements
    gsap.to('.bg-blob', {
        y: '30px',
        rotation: 5,
        duration: 4,
        ease: 'sine.inOut',
        yoyo: true,
        repeat: -1,
        stagger: {
            amount: 2,
            from: "random"
        }
    })
})

useHead({
    title: `${translateLanguage('common.page_not_found')} | Maison El Wali`
})
</script>

<template>
    <div class="error-page" :dir="translateLanguage('common.currency') === 'AED' ? 'rtl' : 'ltr'">
        <!-- Background Elements -->
        <div class="bg-blob blob-1"></div>
        <div class="bg-blob blob-2"></div>
        <div class="bg-blob blob-3"></div>

        <div class="glass-container">
            <div class="content-wrapper">
                <span class="error-code">404</span>
                <h1 class="error-title">{{ translateLanguage('common.page_not_found') }}</h1>
                <p class="error-desc">{{ translateLanguage('common.page_not_found_desc') }}</p>
                
                <div class="actions">
                    <NuxtLink to="/" class="action-btn btn-primary">
                        <span class="btn-icon">🏠</span>
                        {{ translateLanguage('common.go_home') }}
                    </NuxtLink>
                    <NuxtLink to="/catalog" class="action-btn btn-outline">
                        <span class="btn-icon">🔍</span>
                        {{ translateLanguage('search.browse') }}
                    </NuxtLink>
                    <NuxtLink to="/contact" class="action-btn btn-text">
                        {{ translateLanguage('common.report_issue') }}
                    </NuxtLink>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.error-page {
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    background: var(--background);
    padding: 2rem;
}

/* Background Blobs */
.bg-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    z-index: 0;
    opacity: 0.4;
}

.blob-1 {
    width: 400px;
    height: 400px;
    background: var(--primary);
    top: -100px;
    left: -100px;
}

.blob-2 {
    width: 300px;
    height: 300px;
    background: #a855f7; /* Purple accent */
    bottom: -50px;
    right: -50px;
}

.blob-3 {
    width: 200px;
    height: 200px;
    background: #06b6d4; /* Cyan accent */
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    opacity: 0.2;
}

.glass-container {
    position: relative;
    z-index: 1;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 2rem;
    padding: 4rem;
    max-width: 600px;
    width: 100%;
    box-shadow: 
        0 20px 50px rgba(0, 0, 0, 0.05),
        0 1px 3px rgba(0, 0, 0, 0.1),
        inset 0 0 0 1px rgba(255, 255, 255, 0.5);
}

.content-wrapper {
    text-align: center;
}

.error-code {
    display: block;
    font-size: 10rem;
    font-weight: 900;
    line-height: 1;
    background: linear-gradient(135deg, var(--primary) 0%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    letter-spacing: -0.05em;
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
}

.error-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}

.error-desc {
    color: var(--text-muted);
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 2.5rem;
    max-width: 400px;
    margin-left: auto;
    margin-right: auto;
}

.actions {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: center;
}

@media (min-width: 640px) {
    .actions {
        flex-direction: row;
        justify-content: center;
    }
}

.action-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.875rem 1.75rem;
    border-radius: 1rem;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 1rem;
}

.btn-icon {
    font-size: 1.25rem;
}

.btn-primary {
    background: var(--primary);
    color: white;
    box-shadow: 0 4px 12px rgba(var(--primary-rgb), 0.3);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(var(--primary-rgb), 0.4);
}

.btn-outline {
    background: white;
    border: 2px solid var(--border);
    color: var(--text);
}

.btn-outline:hover {
    border-color: var(--primary);
    color: var(--primary);
    transform: translateY(-2px);
    background: var(--primary-light);
}

.btn-text {
    color: var(--text-muted);
    font-size: 0.875rem;
    padding: 0.5rem;
}

.btn-text:hover {
    color: var(--text);
    text-decoration: underline;
}
</style>
