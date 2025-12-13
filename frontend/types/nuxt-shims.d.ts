// Manual shims for Nuxt auto-imports to resolve IDE errors
// caused by broken Node environment preventing generation

declare global {
    // Vue
    const ref: typeof import('vue')['ref']
    const computed: typeof import('vue')['computed']
    const reactive: typeof import('vue')['reactive']
    const onMounted: typeof import('vue')['onMounted']
    const watchEffect: typeof import('vue')['watchEffect']
    const definePageMeta: (meta: any) => void

    // Nuxt
    const useFetch: typeof import('nuxt/app')['useFetch']
    const useHead: typeof import('nuxt/app')['useHead']
    const useRoute: typeof import('vue-router')['useRoute']
    const useRouter: typeof import('vue-router')['useRouter']
    const useRuntimeConfig: () => { public: { apiBase: string } }
    const navigateTo: (to: any) => any
    const $fetch: (url: string, opts?: any) => Promise<any>

    // Local Composables (manual)
    const useApi: () => {
        getProducts: () => any
        getProduct: (id: number) => any
        createProduct: (data: any) => any
        getBrands: () => any
        getCategories: () => any
        getStores: () => any
        getOrders: () => any
        createOrder: (data: any) => any
        login: (u: string, p: string) => any
        getCurrentUser: (token: string) => any
    }
    const useCart: () => any
    const useToast: () => any
}

export { }
