<script setup lang="ts">
import gsap from 'gsap'

definePageMeta({
    layout: 'admin'
})

const api = useApi()
const { data: settingsData } = await api.getSettings()

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
        success('تم حفظ الإعدادات بنجاح')
    } catch (e) {
        const { error } = useToast()
        error('فشل حفظ الإعدادات')
        console.error(e)
    } finally {
        isSaving.value = false
    }
}



onMounted(() => {
    gsap.from('.settings-card', {
        y: 20,
        opacity: 0,
        stagger: 0.1,
        duration: 0.5
    })
})
</script>

<template>
    <div dir="rtl">
            <header class="page-header">
                <div>
                    <h1>الإعدادات</h1>
                    <p class="subtitle">تكوين تفضيلات متجرك</p>
                </div>
                <button class="btn btn-primary" :disabled="isSaving" @click="saveSettings">
                    {{ isSaving ? 'جاري الحفظ...' : 'حفظ التغييرات' }}
                </button>
            </header>

            <div class="settings-grid">
                <!-- Store Information -->
                <div class="settings-card">
                    <h3>معلومات المتجر</h3>
                    <div class="form-group">
                        <label>اسم المتجر</label>
                        <input v-model="settingsMap.store_name" type="text" class="input-field">
                    </div>
                    <div class="form-group">
                        <label>البريد الإلكتروني</label>
                        <input v-model="settingsMap.contact_email" type="email" class="input-field">
                    </div>
                    <div class="form-group">
                        <label>الهاتف</label>
                        <input v-model="settingsMap.contact_phone" type="text" class="input-field">
                    </div>
                    <div class="form-group">
                        <label>العنوان</label>
                        <input v-model="settingsMap.contact_address" type="text" class="input-field">
                    </div>
                </div>

                <!-- Home Page Content -->
                <div class="settings-card">
                    <h3>عرض الصفحة الرئيسية</h3>
                    <div class="form-group">
                        <label>عنوان البانر الرئيسي (HTML مسموح)</label>
                        <input v-model="settingsMap.hero_title" type="text" class="input-field">
                    </div>
                    <div class="form-group">
                        <label>العنوان الفرعي</label>
                        <textarea v-model="settingsMap.hero_subtitle" rows="3" class="input-field"></textarea>
                    </div>
                    <div class="form-group">
                        <label>شارة البانر</label>
                        <input v-model="settingsMap.hero_badge" type="text" class="input-field">
                    </div>
                </div>

                <!-- Theme Customization -->
                <div class="settings-card">
                    <h3>تخصيص المظهر</h3>
                    <div class="form-group">
                        <label>لون أساسي</label>
                        <div class="color-picker-wrapper">
                            <input v-model="settingsMap.theme_primary" type="color" class="color-picker">
                            <input v-model="settingsMap.theme_primary" type="text" class="input-field">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>لون ثانوي</label>
                        <div class="color-picker-wrapper">
                            <input v-model="settingsMap.theme_secondary" type="color" class="color-picker">
                            <input v-model="settingsMap.theme_secondary" type="text" class="input-field">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>لون التمييز (Accent)</label>
                        <div class="color-picker-wrapper">
                            <input v-model="settingsMap.theme_accent" type="color" class="color-picker">
                            <input v-model="settingsMap.theme_accent" type="text" class="input-field">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>الخط الرئيسي</label>
                        <select v-model="settingsMap.theme_font_family" class="input-field">
                            <option value="">افتراضي</option>
                            <option value="'Tajawal', sans-serif">Tajawal</option>
                            <option value="'Cairo', sans-serif">Cairo</option>
                            <option value="'Almarai', sans-serif">Almarai</option>
                        </select>
                    </div>
                </div>



                <!-- Notifications (Future Feature) -->
                <!-- <div class="settings-card"> ... </div> -->
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
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
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

.toggle-group { display: flex; flex-direction: column; gap: 1rem; }
.toggle-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    cursor: pointer;
}
.toggle-item input { width: 18px; height: 18px; }

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
