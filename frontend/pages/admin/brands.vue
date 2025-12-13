<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useApi } from '~/composables/useApi'
import { useToast } from '~/composables/useToast'

definePageMeta({
    layout: 'admin'
})

const api = useApi()
const auth = useAuthStore()
const toast = useToast()

const brands = ref<any[]>([])
const showModal = ref(false)
const isLoading = ref(false)

const form = ref({
    name: '',
    logo_url: ''
})

const fetchBrands = async () => {
    try {
        const { data } = await api.getBrands()
        brands.value = data.value || []
    } catch (e) {
        toast.error('Failed to fetch brands')
    }
}

const handleSubmit = async () => {
    try {
        isLoading.value = true
        await api.createBrand(form.value)
        toast.success('Brand added successfully')
        showModal.value = false
        form.value = { name: '', logo_url: '' }
        await fetchBrands()
    } catch (e: any) {
        toast.error(e.response?._data?.detail || 'Failed to create brand')
    } finally {
        isLoading.value = false
    }
}

const deleteBrand = async (id: number) => {
    if (!confirm('Are you sure you want to delete this brand?')) return
    
    try {
        await api.deleteBrand(id)
        toast.success('Brand deleted')
        await fetchBrands()
    } catch (e: any) {
        toast.error(e.response?._data?.detail || 'Failed to delete brand')
    }
}

onMounted(() => {
    fetchBrands()
})
</script>

<template>
    <div dir="rtl">
        <div class="header">
            <h1>إدارة الماركات</h1>
            <button @click="showModal = true" class="btn btn-primary">+ إضافة ماركة</button>
        </div>

        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>الاسم</th>
                        <th>الشعار</th>
                        <th>إجراءات</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="brand in brands" :key="brand.id">
                        <td>{{ brand.name }}</td>
                        <td>
                            <img v-if="brand.logo_url" :src="brand.logo_url" class="logo-preview" />
                            <span v-else>-</span>
                        </td>
                        <td>
                            <button @click="deleteBrand(brand.id)" class="btn-icon text-danger" title="حذف">
                                🗑️
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Modal -->
        <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
            <div class="modal">
                <h2>إضافة ماركة جديدة</h2>
                <form @submit.prevent="handleSubmit" class="form-grid">
                    <div class="form-group">
                        <label>اسم الماركة</label>
                        <input v-model="form.name" required class="input" />
                    </div>
                     <div class="form-group">
                        <label>رابط الشعار</label>
                        <input v-model="form.logo_url" class="input" />
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" @click="showModal = false" class="btn btn-outline">إلغاء</button>
                        <button type="submit" class="btn btn-primary" :disabled="isLoading">
                            {{ isLoading ? 'جاري الإضافة...' : 'إضافة' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.table-container {
    background: var(--surface);
    border-radius: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    overflow: hidden;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th,
.data-table td {
    padding: 1rem;
    text-align: right;
    border-bottom: 1px solid var(--border);
}

.data-table th {
    background: #f8fafc;
    font-weight: 600;
}

.logo-preview {
    width: 40px;
    height: 40px;
    object-fit: contain;
}

.text-danger { color: var(--danger); }
.btn-icon { background: none; border: none; cursor: pointer; transition: transform 0.2s; }
.btn-icon:hover { transform: scale(1.1); }

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    width: 100%;
    max-width: 500px;
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border);
    border-radius: 0.5rem;
}

.form-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 1.5rem;
}
</style>
