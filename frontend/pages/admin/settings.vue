<script setup lang="ts">
import { gsap } from 'gsap'
const { translateLanguage } = useLanguage()

definePageMeta({
    layout: 'admin'
})

const api = useApi()
const settingsData = ref<any>(null)
const loading = ref(true)
const error = ref<any>(null)

const fetchData = async () => {
    loading.value = true
    error.value = null
    try {
        const { data, error: apiError } = await api.getSettings()
        if (apiError.value) {
            error.value = apiError.value
            return
        }
        settingsData.value = data.value
    } catch (e) {
        error.value = e
    } finally {
        loading.value = false
    }
}

const handleRetry = () => {
    fetchData()
}

// Default structure matching seed data
const settingsMap = reactive<Record<string, string>>({
    store_name: '',
    hero_title: '',
    hero_subtitle: '',
    hero_badge: '',
    contact_email: '',
    contact_phone: '',
    contact_address: '',
    theme_primary: '#10B981',
    theme_secondary: '#1F2937',
    theme_accent: '#F59E0B',
    theme_font_family: ''
})

// Populate map
watchEffect(() => {
    if (settingsData.value) {
        settingsData.value.forEach((s: any) => {
            settingsMap[s.key] = s.value
        })
    }
})

const isSaving = ref(false)

const saveSettings = async () => {
    isSaving.value = true
    try {
        const payload = Object.entries(settingsMap).map(([key, value]) => ({ key, value }))
        await api.updateSettings(payload)
        const { success } = useToast()
        success(translateLanguage('admin.save_success'))
    } catch (e) {
        const { error: toastError } = useToast()
        toastError(translateLanguage('admin.save_failed'))
    } finally {
        isSaving.value = false
    }
}

onMounted(() => {
    fetchData()
    gsap.from('.settings-card', {
        y: 20,
        opacity: 0,
        stagger: 0.1,
        duration: 0.5
    })
})
</script>

<template>
    <div>
        <header class="page-header">
            <div>
                <h1>{{ translateLanguage('admin.settings') }}</h1>
                <p class="subtitle">{{ translateLanguage('nav.admin_portal') }} / {{ translateLanguage('nav.settings') }}</p>
            </div>
            <button class="btn btn-primary" :disabled="isSaving || loading" @click="saveSettings">
                {{ isSaving ? translateLanguage('admin.saving') : translateLanguage('admin.save_changes') }}
            </button>
        </header>

        <!-- Loading State -->
        <PageLoading v-if="loading" :message="translateLanguage('admin.loading_data')" />

        <!-- Error State -->
        <ErrorState 
            v-else-if="error"
            :title="translateLanguage('admin.failed_load')"
            :description="translateLanguage('common.error_desc')"
            :retryable="true"
            @retry="handleRetry"
        >
            <template #footer>
                <div class="error-details">
                    {{ error.message || error.statusText || error }}
                </div>
            </template>
        </ErrorState>

        <div v-else class="settings-grid">
            <!-- Store Information -->
            <div class="settings-card">
                <h3>{{ translateLanguage('admin.store_info') }}</h3>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.name') }}</label>
                    <input v-model="settingsMap.store_name" type="text" class="input-field">
                </div>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.email') }}</label>
                    <input v-model="settingsMap.contact_email" type="email" class="input-field">
                </div>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.phone') }}</label>
                    <input v-model="settingsMap.contact_phone" type="text" class="input-field">
                </div>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.address') }}</label>
                    <input v-model="settingsMap.contact_address" type="text" class="input-field">
                </div>
            </div>

            <!-- Home Page Content -->
            <div class="settings-card">
                <h3>{{ translateLanguage('admin.home_page_content') }}</h3>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.hero_title_label') }}</label>
                    <input v-model="settingsMap.hero_title" type="text" class="input-field">
                </div>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.hero_subtitle_label') }}</label>
                    <textarea v-model="settingsMap.hero_subtitle" rows="3" class="input-field"></textarea>
                </div>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.hero_badge_label') }}</label>
                    <input v-model="settingsMap.hero_badge" type="text" class="input-field">
                </div>
            </div>

            <!-- Theme Customization -->
            <div class="settings-card">
                <h3>{{ translateLanguage('admin.theme_customization') }}</h3>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.primary_color') }}</label>
                    <div class="color-picker-wrapper">
                        <input v-model="settingsMap.theme_primary" type="color" class="color-picker">
                        <input v-model="settingsMap.theme_primary" type="text" class="input-field">
                    </div>
                </div>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.secondary_color') }}</label>
                    <div class="color-picker-wrapper">
                        <input v-model="settingsMap.theme_secondary" type="color" class="color-picker">
                        <input v-model="settingsMap.theme_secondary" type="text" class="input-field">
                    </div>
                </div>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.accent_color') }}</label>
                    <div class="color-picker-wrapper">
                        <input v-model="settingsMap.theme_accent" type="color" class="color-picker">
                        <input v-model="settingsMap.theme_accent" type="text" class="input-field">
                    </div>
                </div>
                <div class="form-group">
                    <label>{{ translateLanguage('admin.main_font') }}</label>
                    <select v-model="settingsMap.theme_font_family" class="input-field">
                        <option value="">{{ translateLanguage('admin.default') }}</option>
                        <option value="'Tajawal', sans-serif">Tajawal</option>
                        <option value="'Cairo', sans-serif">Cairo</option>
                        <option value="'Almarai', sans-serif">Almarai</option>
                    </select>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Page specific styles */

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.subtitle { color: var(--text-muted); margin-top: 0.25rem; }

.settings-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
}

.settings-card {
    background: white;
    border-radius: 1.25rem;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    border: 1px solid var(--border);
    transition: all 0.3s;
}

.settings-card:hover {
    box-shadow: 0 12px 24px rgba(0,0,0,0.06);
}

.settings-card h3 {
    margin-bottom: 1.5rem;
    font-size: 1rem;
}

.form-group { margin-bottom: 1.25rem; }
.form-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: var(--text-muted);
}


.color-picker-wrapper {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}
.color-picker {
    width: 40px;
    height: 40px;
    padding: 0;
    border: none;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
}
</style>
