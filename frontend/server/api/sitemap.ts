export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    // Use the backend URL directly if server-side, or use the proxy
    // During build, we might need direct access if proxy isn't up, 
    // but usually localhost:8000 is fine if running.
    // Use a robust fallback for the API URL
    const apiBase = config.public.apiBase.startsWith('http')
        ? config.public.apiBase
        : (process.env.BACKEND_URL || 'http://localhost:8000')

    try {
        const products: any[] = await $fetch(`${apiBase}/products/`)
        const brands: any[] = await $fetch(`${apiBase}/brands/`)
        const categories: any[] = await $fetch(`${apiBase}/categories/`)

        const urls = []

        // Products
        urls.push(...products.map(p => ({
            loc: `/product/${p.id}`,
            lastmod: p.updated_at || p.created_at,
            changefreq: 'daily',
            priority: 0.8
        })))

        // Static Pages (could be auto-detected but explicit is safe)
        urls.push({ loc: '/', priority: 1.0 })
        urls.push({ loc: '/catalog', priority: 0.9 })
        urls.push({ loc: '/boutique', priority: 0.9 })
        urls.push({ loc: '/about', priority: 0.7 })
        urls.push({ loc: '/contact', priority: 0.7 })

        return urls
    } catch (e) {
        console.error('Sitemap generation failed:', e)
        return []
    }
})
