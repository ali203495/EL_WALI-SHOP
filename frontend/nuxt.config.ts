// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2024-04-03',
    future: {
        compatibilityVersion: 4,
    },
    devtools: { enabled: true },
    modules: [
        '@pinia/nuxt'
    ],
    css: [
        '~/assets/css/main.css'
    ],
    app: {
        head: {
            title: 'MAISON EL WALI - Luxury Gold & Jewelry',
            titleTemplate: '%s | MAISON EL WALI',
            meta: [
                { charset: 'utf-8' },
                { name: 'viewport', content: 'width=device-width, initial-scale=1' },
                { name: 'description', content: 'Discover timeless elegance at Maison El Wali. Premium gold jewelry and exclusive collections for the discerning few.' },
                { name: 'keywords', content: 'gold, jewelry, luxury, dubai, diamonds, el wali, premium' },
                { name: 'author', content: 'Maison El Wali' },
                { name: 'theme-color', content: '#D4AF37' },
                // Open Graph
                { property: 'og:type', content: 'website' },
                { property: 'og:site_name', content: 'Maison El Wali' },
                { property: 'og:title', content: 'MAISON EL WALI - Luxury Gold & Jewelry' },
                { property: 'og:description', content: 'Discover timeless elegance at Maison El Wali. Premium gold jewelry and exclusive collections.' },
                // Twitter Card
                { name: 'twitter:card', content: 'summary_large_image' },
                { name: 'twitter:title', content: 'MAISON EL WALI - Luxury Gold & Jewelry' },
                { name: 'twitter:description', content: 'Discover timeless elegance at Maison El Wali. Premium gold jewelry.' },
            ],
            link: [
                { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
                { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
                { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
            ],
            htmlAttrs: {
                lang: 'en'
            }
        }
    },
    devServer: {
        host: '0.0.0.0',
        port: 3000
    },
    nitro: {
        preset: 'static',
        devProxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                cookieDomainRewrite: "localhost",
                // @ts-expect-error rewrite is valid in http-proxy-middleware used by nitro dev proxy
                rewrite: (path: string) => path.replace(/^\/api/, '')
            }
        }
    },
    runtimeConfig: {
        public: {
            apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api',
            facebookPixelId: process.env.NUXT_PUBLIC_FACEBOOK_PIXEL_ID || ''
        }
    }
})
