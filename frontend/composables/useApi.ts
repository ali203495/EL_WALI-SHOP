import type { Product, Brand, Category, StoreLocation, Order, OrderCreate, TokenResponse, User } from '~/types'

export const useApi = () => {
    const config = useRuntimeConfig()
    // Prioritize runtime config apiBase, fallback to localhost for local dev/prerender if not set
    const baseUrl = config.public.apiBase || 'http://localhost:8000'

    const ping = () => $fetch(`${baseUrl}/`, { method: 'GET' })


    // Catalog
    const getProducts = () => useFetch<Product[]>(`${baseUrl}/products/`)
    const getProduct = (id: number) => useFetch<Product>(`${baseUrl}/products/${id}`)
    const createProduct = (product: Partial<Product>) => {
        const auth = useAuthStore()
        return $fetch<Product>(`${baseUrl}/products/`, {
            method: 'POST',
            body: product,
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }
    const updateProduct = (id: number, product: Partial<Product>) => {
        const auth = useAuthStore()
        return $fetch<Product>(`${baseUrl}/products/${id}`, {
            method: 'PUT',
            body: product,
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }
    const deleteProduct = (id: number) => {
        const auth = useAuthStore()
        return $fetch(`${baseUrl}/products/${id}`, {
            method: 'DELETE',
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }

    // Brands
    const getBrands = () => useFetch<Brand[]>(`${baseUrl}/brands/`)
    const createBrand = (data: Partial<Brand>) => {
        const auth = useAuthStore()
        return $fetch<Brand>(`${baseUrl}/brands/`, {
            method: 'POST',
            body: data,
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }
    const deleteBrand = (id: number) => {
        const auth = useAuthStore()
        return $fetch(`${baseUrl}/brands/${id}`, {
            method: 'DELETE',
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }

    // Categories
    const getCategories = () => useFetch<Category[]>(`${baseUrl}/categories/`, {
        onResponseError({ response: _response }) {
            // console.warn('Failed to fetch categories:', _response.statusText)
        }
    })

    const createCategory = (data: Partial<Category>) => {
        const auth = useAuthStore()
        return $fetch<Category>(`${baseUrl}/categories/`, {
            method: 'POST',
            body: data,
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }
    const deleteCategory = (id: number) => {
        const auth = useAuthStore()
        return $fetch(`${baseUrl}/categories/${id}`, {
            method: 'DELETE',
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }


    // Stores
    const getStores = () => useFetch<StoreLocation[]>(`${baseUrl}/stores/`)
    const createStore = (data: any) => {
        const auth = useAuthStore()
        return $fetch<StoreLocation>(`${baseUrl}/stores/`, {
            method: 'POST',
            body: data,
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }
    const deleteStore = (id: number) => {
        const auth = useAuthStore()
        return $fetch(`${baseUrl}/stores/${id}`, {
            method: 'DELETE',
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }


    // Orders
    const getOrders = () => useFetch<Order[]>(`${baseUrl}/orders/`)
    const createOrder = (order: OrderCreate): Promise<Order> => {
        return $fetch<Order>(`${baseUrl}/orders/`, {
            method: 'POST',
            body: order,
        })
    }

    // Auth
    const login = (username: string, password: string): Promise<TokenResponse> => {
        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)

        return $fetch<TokenResponse>(`${baseUrl}/token`, {
            method: 'POST',
            body: formData,
        })
    }

    const getUsers = () => {
        const auth = useAuthStore()
        return useFetch<User[]>(`${baseUrl}/users/`, {
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }

    const createUser = (userData: any) => {
        const auth = useAuthStore()
        return $fetch<User>(`${baseUrl}/users/`, {
            method: 'POST',
            body: userData,
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }

    const updateUser = (userId: number, userData: any) => {
        const auth = useAuthStore()
        return $fetch<User>(`${baseUrl}/users/${userId}`, {
            method: 'PUT',
            body: userData,
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }

    const deleteUser = (userId: number) => {
        const auth = useAuthStore()
        return $fetch(`${baseUrl}/users/${userId}`, {
            method: 'DELETE',
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }

    const updateUserPassword = (userId: number, password: string) => {
        const auth = useAuthStore()
        return $fetch<User>(`${baseUrl}/users/${userId}/password`, {
            method: 'PUT',
            body: { password },
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }

    const getCurrentUser = (token: string) => {
        return $fetch<User>(`${baseUrl}/users/me`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
    }

    // Settings (CMS)
    const getSettings = () => useFetch<any[]>(`${baseUrl}/settings/`, {
        onResponseError({ response: _response }) {
            // Suppress errors during build/prerender to prevent build failure
            // console.warn('Failed to fetch settings:', _response.statusText)
        }
    })
    const updateSettings = (settings: { key: string, value: string }[]) => $fetch<any[]>(`${baseUrl}/settings/`, {
        method: 'PUT',
        body: settings
    })

    const verifyPassword = (password: string) => $fetch(`${baseUrl}/auth/verify-password`, {
        method: 'POST',
        body: { password }
    })

    const verifySuperCredentials = (credentials: any) => $fetch(`${baseUrl}/auth/verify-super-credentials`, {
        method: 'POST',
        body: credentials
    })

    // Wishlist
    const getWishlist = () => {
        const auth = useAuthStore()
        return useFetch<any[]>(`${baseUrl}/wishlist/`, {
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }
    const addToWishlistApi = (productId: number) => {
        const auth = useAuthStore()
        return $fetch(`${baseUrl}/wishlist/`, {
            method: 'POST',
            body: { product_id: productId },
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }
    const removeFromWishlistApi = (productId: number) => {
        const auth = useAuthStore()
        return $fetch(`${baseUrl}/wishlist/${productId}`, {
            method: 'DELETE',
            headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined
        })
    }

    return {
        getProducts,
        getProduct,
        createProduct,
        updateProduct,
        deleteProduct,
        getBrands,
        getCategories,
        getStores,
        getOrders,
        createOrder,
        login,
        getUsers,
        createUser,
        updateUser,
        deleteUser,
        updateUserPassword,
        getCurrentUser,
        getSettings,
        updateSettings,
        getWishlist,
        createBrand,
        deleteBrand,
        createCategory,
        deleteCategory,
        createStore,
        deleteStore,
        addToWishlistApi,
        removeFromWishlistApi,
        verifyPassword,
        verifySuperCredentials,
        uploadImage: async (file: File) => {
            const formData = new FormData()
            formData.append('file', file)
            const result = await $fetch<{ url: string }>(`${baseUrl}/upload/`, {
                method: 'POST',
                body: formData
            })
            return result.url
        },
        ping
    }
}
