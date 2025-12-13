import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
    const token = useCookie<string | null>('auth_token', {
        maxAge: 60 * 60 * 24 * 7, // 1 week
        watch: true
    })
    const user = ref<any | null>(null)

    const isAuthenticated = computed(() => !!token.value)

    async function login(username: string, password: string) {
        const api = useApi()
        try {
            const data = await api.login(username, password)
            if (data.access_token) {
                token.value = data.access_token
                await fetchUser()
                return true
            }
        } catch (e) {
            console.error(e)
            return false
        }
        return false
    }

    async function fetchUser() {
        if (!token.value) return
        const api = useApi()
        try {
            user.value = await api.getCurrentUser(token.value)
        } catch (e) {
            logout()
        }
    }

    function logout() {
        token.value = null
        user.value = null
        navigateTo('/')
    }

    // Try to fetch user on init if token exists
    if (token.value) {
        fetchUser()
    }

    return {
        token,
        user,
        isAuthenticated,
        login,
        fetchUser,
        logout
    }
})
