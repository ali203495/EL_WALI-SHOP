<script setup lang="ts">
const { translateLanguage } = useLanguage()
const auth = useAuthStore()
const api = useApi()
const toast = useToast()

definePageMeta({
    layout: 'account',
    middleware: ['auth']
})

const form = reactive({
    first_name: auth.user?.first_name || '',
    last_name: auth.user?.last_name || '',
    email: auth.user?.email || '',
    password: '' // Optional logic for password change could be added
})

const loading = ref(false)

const handleUpdate = async () => {
    if (!auth.user?.id) return
    
    loading.value = true
    try {
        const updated = await api.updateUser(auth.user.id, {
            first_name: form.first_name,
            last_name: form.last_name,
            email: form.email
            // Password logic separate usually
        })
        
        // Update local store
        auth.user = { ...auth.user, ...updated }
        toast.success(translateLanguage('account.save_success'))
    } catch (e) {
        toast.error(translateLanguage('account.save_failed'))
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="settings-page">
        <header class="section-header">
            <h1>{{ translateLanguage('account.account_settings') }}</h1>
        </header>

        <form class="settings-form" @submit.prevent="handleUpdate">
            <div class="form-row">
                <div class="form-group">
                    <label>{{ translateLanguage('account.first_name') }}</label>
                    <input v-model="form.first_name" type="text" class="input-field" required>
                </div>
                <div class="form-group">
                    <label>{{ translateLanguage('account.last_name') }}</label>
                    <input v-model="form.last_name" type="text" class="input-field" required>
                </div>
            </div>

            <div class="form-group">
                <label>{{ translateLanguage('common.email') }}</label>
                <input v-model="form.email" type="email" class="input-field" required dir="ltr">
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary" :disabled="loading">
                    {{ loading ? translateLanguage('account.saving') : translateLanguage('account.save_changes') }}
                </button>
            </div>
        </form>
    </div>
</template>

<style scoped>
.section-header {
    margin-bottom: 2rem;
}

.settings-form {
    max-width: 600px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.form-actions {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}

@media (max-width: 600px) {
    .form-row {
        grid-template-columns: 1fr;
    }
}
</style>
