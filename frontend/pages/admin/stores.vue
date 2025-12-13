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

const stores = ref<any[]>([])
const showModal = ref(false)
const isLoading = ref(false)

const form = ref({
    name: '',
    address: '',
    city: '',
    phone: '',
    latitude: 0,
    longitude: 0
})

const fetchStores = async () => {
    try {
        const { data } = await api.getStores()
        stores.value = data.value || []
    } catch (e) {
        toast.error('Failed to fetch stores')
    }
}

const handleSubmit = async () => {
    try {
        isLoading.value = true
        await api.createStore(form.value)
        toast.success('Store added successfully')
        showModal.value = false
        form.value = { name: '', address: '', city: '', phone: '', latitude: 0, longitude: 0 }
        await fetchStores()
    } catch (e: any) {
        toast.error(e.response?._data?.detail || 'Failed to create store')
    } finally {
        isLoading.value = false
    }
}

const deleteStore = async (id: number) => {
    if (!confirm('Are you sure you want to delete this store?')) return
    
    try {
        await api.deleteStore(id)
        toast.success('Store deleted')
        await fetchStores()
    } catch (e: any) {
        toast.error(e.response?._data?.detail || 'Failed to delete store')
    }
}

onMounted(() => {
    fetchStores()
})
</script>

<template>
    <div dir="rtl">
        <div class="header">
            <h1>إدارة المتاجر</h1>
            <button @click="showModal = true" class="btn btn-primary">+ إضافة متجر</button>
        </div>

        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>الاسم</th>
                        <th>العنوان</th>
                        <th>المدينة</th>
                        <th>الهاتف</th>
                        <th>إجراءات</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="store in stores" :key="store.id">
                        <td>{{ store.name }}</td>
                        <td>{{ store.address }}</td>
                        <td>{{ store.city }}</td>
                        <td>{{ store.phone }}</td>
                        <td>
                            <button @click="deleteStore(store.id)" class="btn-icon text-danger" title="حذف">
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
                <h2>إضافة متجر جديد</h2>
                <form @submit.prevent="handleSubmit" class="form-grid">
                    <div class="form-group">
                        <label>اسم المتجر</label>
                        <input v-model="form.name" required class="input" />
                    </div>
                    
                    <div class="form-group">
                        <label>العنوان</label>
                        <input v-model="form.address" required class="input" />
                    </div>
                    
                    <div class="form-group">
                        <label>المدينة</label>
                        <input v-model="form.city" required class="input" />
                    </div>
                    
                     <div class="form-group">
                        <label>الهاتف</label>
                        <input v-model="form.phone" class="input" />
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
