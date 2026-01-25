export default defineNuxtRouteMiddleware((_to, _from) => {
    const auth = useAuthStore()

    // access_token check or store state check
    if (!auth.token && !auth.user) {
        return navigateTo('/login')
    }
})
