
import { reactive, toRefs } from 'vue'

// Define default settings to avoid empty UI before load
const defaultSettings = {
    // Branding
    store_name: 'Maison El Wali',

    // Theme
    theme_primary: '#10B981', // Default Emerald
    theme_secondary: '#1F2937',
    theme_accent: '#F59E0B',
    theme_font_family: '',

    // Contact
    contact_email: 'info@maisonelwali.com',
    contact_phone: '+971 4 123 4567',
    contact_address: '12 Royal Palm Avenue, Dubai, UAE',
    whatsapp_number: '',

    // Home Hero
    hero_title: 'Timeless Elegance',
    hero_subtitle: 'Curated collections of the finest gold and diamond jewelry for the modern connoisseur.',
    hero_badge: 'Maison El Wali'
}

const state = reactive({
    settings: { ...defaultSettings },
    loading: false,
    initialized: false
})

export const useSiteSettings = () => {
    const api = useApi()

    const applyTheme = () => {
        if (import.meta.server) return

        const root = document.documentElement
        if (state.settings.theme_primary) {
            root.style.setProperty('--primary', state.settings.theme_primary)
        }
        if (state.settings.theme_secondary) {
            root.style.setProperty('--secondary', state.settings.theme_secondary)
        }
        if (state.settings.theme_font_family) {
            root.style.setProperty('--font-primary', state.settings.theme_font_family)
        }
    }

    const init = async () => {
        if (state.initialized) return

        state.loading = true
        try {
            const { data, error } = await api.getSettings()

            if (error.value) {
                // console.warn('Failed to fetch settings:', error.value)
                return
            }

            if (data.value) {
                // Map array of {key, value} to object
                const settingsMap: Record<string, string> = {}
                data.value.forEach((s: any) => {
                    settingsMap[s.key] = s.value
                })

                // Merge with defaults
                state.settings = { ...state.settings, ...settingsMap }
                applyTheme()
            }
        } catch (e) {
            // console.error('Failed to load site settings', e)
        } finally {
            state.loading = false
            state.initialized = true
        }
    }

    return {
        ...toRefs(state),
        init,
        applyTheme
    }
}
