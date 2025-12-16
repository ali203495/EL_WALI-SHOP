<script setup lang="ts">
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
        toast.success('تم تحديث البيانات بنجاح')
    } catch (e) {
        toast.error('حدث خطأ أثناء التحديث')
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="settings-page">
        <header class="section-header">
            <h1>إعدادات الحساب</h1>
        </header>

        <form @submit.prevent="handleUpdate" class="settings-form">
            <div class="form-row">
                <div class="form-group">
                    <label>الاسم الأول</label>
                    <input v-model="form.first_name" type="text" class="input-field" required>
                </div>
                <div class="form-group">
                    <label>اسم العائلة</label>
                    <input v-model="form.last_name" type="text" class="input-field" required>
                </div>
            </div>

            <div class="form-group">
                <label>البريد الإلكتروني</label>
                <input v-model="form.email" type="email" class="input-field" required dir="ltr">
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary" :disabled="loading">
                    {{ loading ? 'جاري الحفظ...' : 'حفظ التغييرات' }}
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
