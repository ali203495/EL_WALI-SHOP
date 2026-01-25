interface CartItem {
    product: {
        id: number
        name: string
        price: number
        image_url: string
        stock: number
    }
    quantity: number
}

const cart = ref<CartItem[]>([])

// Load from localStorage on client side
if (import.meta.client) {
    const saved = localStorage.getItem('cart')
    if (saved) {
        try {
            cart.value = JSON.parse(saved)
        } catch (e) {
            // console.error('Failed to parse cart', e)
        }
    }
}

// Watch for changes
watch(cart, (newCart) => {
    if (import.meta.client) {
        localStorage.setItem('cart', JSON.stringify(newCart))
    }
}, { deep: true })

export const useCart = () => {
    const addToCart = (product: CartItem['product'], requestedQty: number = 1) => {
        const existing = cart.value.find(item => item.product.id === product.id)

        if (existing) {
            const newQty = existing.quantity + requestedQty
            if (newQty <= product.stock) {
                existing.quantity = newQty
            } else {
                existing.quantity = product.stock // Cap at stock
            }
        } else {
            const quantity = Math.min(requestedQty, product.stock)
            cart.value.push({ product, quantity })
        }
    }

    const removeFromCart = (productId: number) => {
        const index = cart.value.findIndex(item => item.product.id === productId)
        if (index > -1) {
            cart.value.splice(index, 1)
        }
    }

    const updateQuantity = (productId: number, quantity: number) => {
        const item = cart.value.find(i => i.product.id === productId)
        if (item) {
            if (quantity <= 0) {
                removeFromCart(productId)
            } else if (quantity <= item.product.stock) {
                item.quantity = quantity
            }
        }
    }

    const clearCart = () => {
        cart.value = []
    }

    const subtotal = computed(() => {
        return cart.value.reduce((sum, item) => sum + (item.product.price * item.quantity), 0)
    })

    const taxRate = 0.08 // 8%
    const tax = computed(() => subtotal.value * taxRate)
    const total = computed(() => subtotal.value + tax.value)

    const itemCount = computed(() => {
        return cart.value.reduce((sum, item) => sum + item.quantity, 0)
    })

    return {
        cart: readonly(cart),
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        subtotal,
        tax,
        total,
        itemCount,
    }
}
