<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'
import { useToast } from '~/composables/useToast'

useHead({
    title: 'Forgot Password',
    meta: [{ name: 'robots', content: 'noindex, nofollow' }]
})

definePageMeta({
    layout: false
})

const toast = useToast()
const route = useRoute()

const step = ref(1) // 1: Email, 2: Code & New Password
const email = ref('')
const code = ref('')
const newPassword = ref('')
const isLoading = ref(false)

const handleRequestCode = async () => {
    isLoading.value = true
    try {
        // Use $fetch directly since useApi doesn't expose generic post
        const config = useRuntimeConfig()
        await $fetch(`${config.public.apiBase}/auth/forgot-password`, {
            method: 'POST',
            body: { email: email.value }
        })
        toast.success('Verification code sent if email exists')
        step.value = 2
        
        // Animate transition
        gsap.from('.step-2', {
            x: 20,
            opacity: 0,
            duration: 0.4
        })
    } catch (e) {
        toast.error('Failed to process request')
    } finally {
        isLoading.value = false
    }
}

const handleResetPassword = async () => {
    isLoading.value = true
    try {
        const config = useRuntimeConfig()
        await $fetch(`${config.public.apiBase}/auth/reset-password`, {
             method: 'POST',
             body: {
                email: route.query.email,
                code: code.value,
                new_password: newPassword.value
            }
        })
        toast.success('Password updated successfully')
        navigateTo('/login')
    } catch (e: any) {
        toast.error(e.response?._data?.detail || 'Failed to reset password')
    } finally {
        isLoading.value = false
    }
}

onMounted(() => {
    gsap.from('.card', { y: 30, opacity: 0, duration: 0.6, ease: 'power2.out' })
})
</script>

<template>
    <div class="page-container">
        <div class="background">
             <div class="gradient-orb orb-1"></div>
        </div>
        
        <div class="card">
            <h2>Reset Password</h2>
            
            <div v-if="step === 1">
                <p class="subtitle">Enter your email to receive a recovery code.</p>
                <form @submit.prevent="handleRequestCode">
                    <div class="form-group">
                        <label>Email Address</label>
                        <input v-model="email" type="email" required class="input" placeholder="admin@example.com" />
                    </div>
                    
                    <button type="submit" class="btn btn-primary full-width" :disabled="isLoading">
                        {{ isLoading ? 'Sending...' : 'Send Code' }}
                    </button>
                </form>
            </div>
            
            <div v-if="step === 2" class="step-2">
                <p class="subtitle">Enter the code sent to your email and your new password.</p>
                <form @submit.prevent="handleResetPassword">
                    <div class="form-group">
                        <label>Verification Code</label>
                        <input v-model="code" required class="input" placeholder="123456" />
                    </div>
                    
                    <div class="form-group">
                        <label>New Password</label>
                        <input v-model="newPassword" type="password" required class="input" placeholder="New password" />
                    </div>
                    
                    <button type="submit" class="btn btn-primary full-width" :disabled="isLoading">
                        {{ isLoading ? 'Updating...' : 'Update Password' }}
                    </button>
                </form>
            </div>
            
            <NuxtLink to="/login" class="back-link">Back to Login</NuxtLink>
        </div>
    </div>
</template>

<style scoped>
.page-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0f172a;
    position: relative;
    overflow: hidden;
}

.background {
    position: absolute;
    inset: 0;
}

.gradient-orb {
    position: absolute;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, rgba(0, 0, 0, 0) 70%);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.card {
    background: white;
    padding: 2.5rem;
    border-radius: 1rem;
    width: 100%;
    max-width: 400px;
    position: relative;
    z-index: 10;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

h2 {
    text-align: center;
    margin-bottom: 0.5rem;
    font-size: 1.5rem;
    font-weight: 700;
}

.subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 1.5rem;
    font-size: 0.875rem;
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    font-size: 0.875rem;
}

.input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    transition: border-color 0.2s;
}

.input:focus {
    border-color: #4f46e5;
    outline: none;
}

.btn {
    padding: 0.75rem;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
    transition: opacity 0.2s;
}

.btn-primary {
    background: #4f46e5;
    color: white;
}

.btn-primary:active {
    opacity: 0.9;
}

.full-width {
    width: 100%;
    margin-top: 0.5rem;
}

.back-link {
    display: block;
    text-align: center;
    margin-top: 1.5rem;
    color: #64748b;
    text-decoration: none;
    font-size: 0.875rem;
}

.back-link:hover {
    color: #4f46e5;
}
</style>
