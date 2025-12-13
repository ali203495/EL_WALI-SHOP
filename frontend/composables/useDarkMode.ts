const isDark = ref(false)

export const useDarkMode = () => {
    const toggle = () => {
        isDark.value = !isDark.value
        updateDOM()
        savePreference()
    }

    const updateDOM = () => {
        if (process.client) {
            document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
        }
    }

    const savePreference = () => {
        if (process.client) {
            localStorage.setItem('darkMode', String(isDark.value))
        }
    }

    const loadPreference = () => {
        if (process.client) {
            const saved = localStorage.getItem('darkMode')
            if (saved !== null) {
                isDark.value = saved === 'true'
            } else {
                // Check system preference
                isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
            }
            updateDOM()
        }
    }

    // Auto-load on mount
    onMounted(loadPreference)

    return {
        isDark: readonly(isDark),
        toggle,
    }
}
