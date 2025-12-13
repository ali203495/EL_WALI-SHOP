
export const useWishlist = () => {
    const api = useApi()
    const { $toast } = useNuxtApp()

    // State
    const items = useState<any[]>('wishlist_items', () => [])
    const isLoading = useState('wishlist_loading', () => false)

    // Actions
    const fetchWishlist = async () => {
        isLoading.value = true
        try {
            const { data } = await api.getWishlist()
            items.value = data.value || []
        } catch (e) {
            console.error('Failed to fetch wishlist', e)
        } finally {
            isLoading.value = false
        }
    }

    const addToWishlist = async (productId: number) => {
        // Optimistic update check
        if (isInWishlist(productId)) return

        isLoading.value = true
        try {
            const res = await api.addToWishlistApi(productId)
            items.value.push(res)
            $toast.success('Added to wishlist')
        } catch (e: any) {
            // $toast.error(e.response?._data?.detail || 'Failed to add to wishlist')
            console.error(e)
        } finally {
            isLoading.value = false
        }
    }

    const removeFromWishlist = async (productId: number) => {
        isLoading.value = true
        try {
            await api.removeFromWishlistApi(productId)
            items.value = items.value.filter(i => i.product.id !== productId)
            $toast.info('Removed from wishlist')
        } catch (e) {
            // $toast.error('Failed to remove from wishlist')
            console.error(e)
        } finally {
            isLoading.value = false
        }
    }

    const isInWishlist = (productId: number) => {
        return items.value.some(i => i.product.id === productId)
    }

    const toggleWishlist = (productId: number) => {
        if (isInWishlist(productId)) {
            removeFromWishlist(productId)
        } else {
            addToWishlist(productId)
        }
    }

    return {
        items,
        isLoading,
        fetchWishlist,
        addToWishlist,
        removeFromWishlist,
        isInWishlist,
        toggleWishlist
    }
}
