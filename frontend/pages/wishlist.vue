<script setup lang="ts">
import gsap from 'gsap'

const { fetchWishlist, items, isLoading, removeFromWishlist } = useWishlist()
const { addToCart } = useCart()

onMounted(async () => {
    await fetchWishlist()
    
    gsap.from('.wishlist-item', {
        y: 20,
        opacity: 0,
        stagger: 0.1,
        duration: 0.5
    })
})
</script>

<template>
    <div class="wishlist-page">
        <div class="container mx-auto px-4 py-8">
            <h1 class="text-3xl font-bold mb-6">قائمة الرغبات</h1>
            
            <div v-if="isLoading && items.length === 0" class="flex justify-center py-12">
                <Spinner />
            </div>

            <div v-else-if="items.length === 0" class="empty-state text-center py-12">
                <div class="text-6xl mb-4">💔</div>
                <h2 class="text-xl font-semibold mb-2">قائمة الرغبات فارغة</h2>
                <p class="text-gray-500 mb-6">لم تقم بإضافة أي منتجات بعد</p>
                <NuxtLink to="/catalog" class="btn btn-primary">تصفح المنتجات</NuxtLink>
            </div>

            <div v-else class="wishlist-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="item in items" :key="item.id" class="wishlist-item bg-white rounded-lg shadow-sm p-4 flex gap-4">
                    <img :src="item.product.image_url" :alt="item.product.name" class="w-24 h-24 object-cover rounded-md">
                    <div class="flex-1 flex flex-col justify-between">
                        <div>
                            <h3 class="font-semibold text-lg">{{ item.product.name }}</h3>
                            <p class="text-primary font-bold mt-1">${{ item.product.price }}</p>
                        </div>
                        <div class="flex gap-2 mt-4">
                            <button @click="addToCart(item.product)" class="btn btn-sm btn-primary flex-1">
                                إضافة للسلة
                            </button>
                            <button @click="removeFromWishlist(item.product.id)" class="btn btn-sm btn-outline text-red-500 border-red-500 hover:bg-red-50">
                                حذف
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
