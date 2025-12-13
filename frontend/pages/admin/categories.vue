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

const categories = ref<any[]>([])
const showModal = ref(false)
const isLoading = ref(false)

const form = ref({
    name: ''
})

const fetchCategories = async () => {
    try {
        const { data } = await api.getCategories()
        categories.value = data.value || []
    } catch (e) {
        toast.error('Failed to fetch categories')
    }
}

const handleSubmit = async () => {
    try {
        isLoading.value = true
        await api.createCategory(form.value)
        toast.success('Category added successfully')
        showModal.value = false
        form.value.name = ''
        await fetchCategories()
    } catch (e: any) {
        toast.error(e.response?._data?.detail || 'Failed to create category')
    } finally {
        isLoading.value = false
    }
}

const deleteCategory = async (id: number) => {
    if (!confirm('Are you sure you want to delete this category?')) return
    
    try {
        await api.deleteCategory(id)
        toast.success('Category deleted')
        await fetchCategories()
    } catch (e: any) {
        toast.error(e.response?._data?.detail || 'Failed to delete category')
    }
}

onMounted(() => {
    fetchCategories()
})
</script>

<template>
    <div dir="rtl">
        <div class="header">
            <h1>إدارة الفئات</h1>
            <button @click="showModal = true" class="btn btn-primary">+ إضافة فئة</button>
        </div>

        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>الاسم</th>
                        <th>إجراءات</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="category in categories" :key="category.id">
                        <td>{{ category.name }}</td>
                        <td>
                            <button @click="deleteCategory(category.id)" class="btn-icon text-danger" title="حذف">
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
                <h2>إضافة فئة جديدة</h2>
                <form @submit.prevent="handleSubmit" class="form-grid">
                    <div class="form-group">
                        <label>اسم الفئة</label>
                        <input v-model="form.name" required class="input" />
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
