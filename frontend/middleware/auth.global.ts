export default defineNuxtRouteMiddleware(async (to, _from) => {
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
        // If logged in but user info not fetched yet -> Wait for it
        if (auth.isAuthenticated && !auth.user) {
            await auth.fetchUser()
        }

        const allowedUsers = ['admin', 'abdelaali']
        const username = auth.user?.username?.toLowerCase()

        // If logged in but not an authorized admin -> Redirect to Home
        if (auth.isAuthenticated && (!username || !allowedUsers.includes(username))) {
            return navigateTo('/')
        }
    }
})
