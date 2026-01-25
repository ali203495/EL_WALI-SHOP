<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'
import { useAuthStore } from '~/stores/auth'
const { translateLanguage } = useLanguage()

useHead({
    title: translateLanguage('admin.admin_login'),
    meta: [
        { name: 'robots', content: 'noindex, nofollow' }
    ]
})

definePageMeta({
    layout: false // Full page login
})

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const error = ref('')
const auth = useAuthStore()
const { ping } = useApi()
const backendStatus = ref<'checking' | 'online' | 'offline'>('checking')

const checkBackend = async () => {
    try {
        await ping()
        backendStatus.value = 'online'
    } catch (e) {
        // console.error('Backend unreachable:', e)
        backendStatus.value = 'offline'
    }
}

onMounted(() => {
    checkBackend()
    gsap.from('.login-card', {
        y: 60,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out'
    })
    gsap.from('.brand-logo', {
        scale: 0.8,
        opacity: 0,
        duration: 0.6,
        ease: 'back.out(1.7)'
    })
})

const handleLogin = async () => {
    error.value = ''
    isLoading.value = true
    
    try {
        const success = await auth.login(username.value, password.value)
        if (success) {
            gsap.to('.login-card', {
                scale: 0.95,
                opacity: 0,
                duration: 0.3,
                onComplete: () => navigateTo('/admin')
            } as any)
        } else {
            error.value = translateLanguage('admin.invalid_credentials')
            gsap.to('.login-card', {
                x: [-10, 10, -10, 10, 0],
                duration: 0.4,
            } as any)
        }
    } finally {
        isLoading.value = false
    }
}
</script>

<template>
    <div class="login-page">
        <div class="login-background">
            <div class="gradient-orb orb-1"></div>
            <div class="gradient-orb orb-2"></div>
        </div>

        <div class="lang-switcher-wrapper">
            <LanguageSwitcher />
        </div>
        
        <div class="login-content">
            <div class="brand-logo">
                <h1>MAISON <span>EL WALI</span></h1>
            </div>
            
            <div class="login-card">
                <div class="backend-status-badge" :class="backendStatus">
                    <span class="dot"></span>
                    {{ backendStatus === 'online' ? translateLanguage('admin.backend_online') : backendStatus === 'offline' ? translateLanguage('admin.backend_offline') : translateLanguage('admin.checking_connectivity') }}
                </div>
                <h2>{{ translateLanguage('admin.welcome_back') }}</h2>
                <p class="subtitle">{{ translateLanguage('admin.sign_in_subtitle') }}</p>
                
                <div class="form-group">
                    <label>{{ translateLanguage('admin.username') }}</label>
                    <input 
                        v-model="username" 
                        class="input-field" 
                        type="text" 
                        :placeholder="translateLanguage('admin.search_placeholder').replace('...', '')"
                        @keyup.enter="handleLogin"
                    />
                </div>
                
                <div class="form-group">
                    <label>{{ translateLanguage('admin.password') }}</label>
                    <input 
                        v-model="password" 
                        class="input-field" 
                        type="password" 
                        :placeholder="translateLanguage('admin.password')"
                        @keyup.enter="handleLogin"
                    />
                </div>

                <div class="forgot-password">
                    <NuxtLink to="/forgot-password">{{ translateLanguage('admin.forgot_password') }}</NuxtLink>
                </div>
                
                <p v-if="error" class="error-message">{{ error }}</p>
                
                <button 
                    class="btn btn-primary btn-lg login-btn" 
                    :disabled="isLoading || !username || !password || backendStatus === 'offline'"
                    @click="handleLogin"
                >
                    <span v-if="isLoading">{{ translateLanguage('admin.signing_in') }}</span>
                    <span v-else>{{ translateLanguage('admin.sign_in') }}</span>
                </button>
                
            </div>
            
            <NuxtLink to="/" class="back-link">← {{ translateLanguage('common.back_to_store') }}</NuxtLink>
        </div>
    </div>
</template>

<style scoped>
.lang-switcher-wrapper {
    position: absolute;
    top: 1rem;
    right: 1rem;
    z-index: 100;
}
.login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0f172a;
    overflow: hidden;
    position: relative;
}

.login-background {
    position: absolute;
    inset: 0;
    overflow: hidden;
}

.gradient-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    opacity: 0.4;
}

.orb-1 {
    width: 600px;
    height: 600px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    top: -200px;
    right: -100px;
}

.orb-2 {
    width: 400px;
    height: 400px;
    background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
    bottom: -100px;
    left: -100px;
}

.login-content {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.brand-logo h1 {
    color: white;
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 2rem;
}

.brand-logo span {
    color: var(--primary);
}

.login-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 1.5rem;
    padding: 3rem;
    width: 420px;
    max-width: 90vw;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    position: relative;
}

.backend-status-badge {
    position: absolute;
    top: 1rem;
    right: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    background: #f1f5f9;
    color: #64748b;
}

.backend-status-badge.online {
    background: #f0fdf4;
    color: #166534;
}

.backend-status-badge.offline {
    background: #fef2f2;
    color: #991b1b;
}

.backend-status-badge .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #94a3b8;
}

.backend-status-badge.online .dot {
    background: #22c55e;
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

.backend-status-badge.offline .dot {
    background: #ef4444;
}

.login-card h2 {
    text-align: center;
    margin-bottom: 0.5rem;
    font-size: 1.75rem;
}

.subtitle {
    text-align: center;
    color: var(--text-muted);
    margin-bottom: 2rem;
}

.form-group {
    margin-bottom: 1.25rem;
}

.form-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.login-btn {
    width: 100%;
    margin-top: 1rem;
}

.error-message {
    color: #ef4444;
    text-align: center;
    font-size: 0.875rem;
    margin-bottom: 1rem;
    padding: 0.75rem;
    background: #fef2f2;
    border-radius: 0.5rem;
}

.demo-hint {
    text-align: center;
    margin-top: 1.5rem;
    font-size: 0.875rem;
    color: var(--text-muted);
}

.demo-hint code {
    background: #f1f5f9;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-family: monospace;
}

.back-link {
    margin-top: 2rem;
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    font-size: 0.875rem;
    transition: color 0.2s;
}

.back-link:hover {
    color: white;
}

.forgot-password {
    text-align: right;
    margin-bottom: 1.5rem;
}

.forgot-password a {
    color: var(--primary);
    font-size: 0.875rem;
    text-decoration: none;
}

.forgot-password a:hover {
    text-decoration: underline;
}
</style>
