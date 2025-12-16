export default defineNuxtRouteMiddleware((to, from) => {
    const auth = useAuthStore()

    // access_token check or store state check
    if (!auth.token && !auth.user) {
        return navigateTo('/login')
    }
})
