export default defineNuxtRouteMiddleware((to, from) => {
    const auth = useAuthStore()

    // 1. Define protected routes (Admin & Account)
    const protectedPrefixes = ['/admin', '/account']
    const isProtected = protectedPrefixes.some(prefix => to.path.startsWith(prefix))

    // 2. If trying to access protected route and not logged in
    if (isProtected && !auth.isAuthenticated) {
        // Build redirect with 'redirect' query param to return after login
        return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
    }

    // 3. Specific Admin Security Check
    if (to.path.startsWith('/admin')) {
        const allowedUsers = ['admin', 'Abdelaali']
        // If logged in but not an admin -> Redirect to Home
        if (auth.isAuthenticated && (!auth.user?.username || !allowedUsers.includes(auth.user.username))) {
            return navigateTo('/')
        }
    }
})
