<script setup lang="ts">
interface ProductForm {
    id?: number
    name: string
    description: string
    price: number
    stock: number
    image_url: string
    category_id: number | null
    brand_id: number | null
}

const props = defineProps<{
    product?: ProductForm
    categories: { id: number; name: string }[]
    brands: { id: number; name: string }[]
}>()

const emit = defineEmits<{
    (e: 'submit', data: ProductForm): void
    (e: 'cancel'): void
}>()

const form = reactive<ProductForm>({
    id: props.product?.id,
    name: props.product?.name || '',
    description: props.product?.description || '',
    price: props.product?.price || 0,
    stock: props.product?.stock || 0,
    image_url: props.product?.image_url || '',
    category_id: props.product?.category_id || null,
    brand_id: props.product?.brand_id || null,
})

const isEdit = computed(() => !!props.product?.id)

const api = useApi()
const imageType = ref<'url' | 'upload'>('url')
const uploading = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const handleSubmit = () => {
    emit('submit', { ...form })
}

const handleFileUpload = async (event: Event) => {
    const target = event.target as HTMLInputElement
    if (target.files && target.files[0]) {
        uploading.value = true
        try {
            const url = await api.uploadImage(target.files[0])
            form.image_url = url
        } catch (e) {
            alert('Fialed to upload image')
        } finally {
            uploading.value = false
        }
    }
}
</script>

<template>
    <form @submit.prevent="handleSubmit" class="product-form" dir="rtl">
        <div class="form-grid">
            <div class="form-group full-width">
                <label>اسم المنتج *</label>
                <input v-model="form.name" type="text" required class="input-field">
            </div>
            
            <div class="form-group full-width">
                <label>الوصف</label>
                <textarea v-model="form.description" rows="3" class="input-field"></textarea>
            </div>
            
            <div class="form-group">
                <label>السعر *</label>
                <input v-model="form.price" type="number" min="0" step="0.01" required class="input-field">
            </div>
            
            <div class="form-group">
                <label>المخزون *</label>
                <input v-model="form.stock" type="number" min="0" required class="input-field">
            </div>
            
            <div class="form-group">
                <label>الفئة</label>
                <select v-model="form.category_id" class="input-field">
                    <option :value="null">اختر الفئة</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                        {{ cat.name }}
                    </option>
                </select>
            </div>
            
            <div class="form-group">
                <label>الماركة</label>
                <select v-model="form.brand_id" class="input-field">
                    <option :value="null">اختر الماركة</option>
                    <option v-for="brand in brands" :key="brand.id" :value="brand.id">
                        {{ brand.name }}
                    </option>
                </select>
            </div>
            
            <div class="form-group full-width">
                <label>صورة المنتج</label>
                
                <div class="image-input-type">
                    <button type="button" 
                        class="type-btn" 
                        :class="{ active: imageType === 'url' }"
                        @click="imageType = 'url'"
                    >
                        رابط خارجي
                    </button>
                    <button type="button" 
                        class="type-btn" 
                        :class="{ active: imageType === 'upload' }"
                        @click="imageType = 'upload'"
                    >
                        رفع صورة
                    </button>
                </div>

                <div v-if="imageType === 'url'" class="mt-2">
                    <input v-model="form.image_url" type="url" placeholder="https://..." class="input-field" style="direction: ltr; text-align: left;">
                </div>

                <div v-else class="mt-2 upload-container">
                    <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" class="file-input">
                    <div v-if="uploading" class="upload-status">جاري الرفع...</div>
                    <div v-if="form.image_url && imageType === 'upload'" class="preview">
                        <img :src="form.image_url" alt="Preview">
                    </div>
                </div>
            </div>
        </div>
        
        <div class="form-actions">
            <button type="button" class="btn btn-outline" @click="emit('cancel')">إلغاء</button>
            <button type="submit" class="btn btn-primary">
                {{ isEdit ? 'تحديث المنتج' : 'إضافة المنتج' }}
            </button>
        </div>
    </form>
</template>

<style scoped>
.product-form {
    padding: 1rem 0;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.full-width {
    grid-column: 1 / -1;
}

.form-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 700; /* Bold for contrast */
    color: var(--text);   /* Adapts to theme */
    margin-bottom: 0.5rem;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}

.image-input-type {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.type-btn {
    padding: 0.5rem 1rem;
    background: transparent;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    cursor: pointer;
    font-size: 0.875rem;
}

.type-btn.active {
    background: var(--primary-light);
    color: var(--primary);
    border-color: var(--primary);
    font-weight: 600;
}

.mt-2 { margin-top: 0.5rem; }

.upload-container {
    border: 2px dashed var(--border);
    padding: 1rem;
    border-radius: var(--radius);
    text-align: center;
}

.preview img {
    max-height: 100px;
    margin-top: 1rem;
    border-radius: var(--radius);
}
</style>
