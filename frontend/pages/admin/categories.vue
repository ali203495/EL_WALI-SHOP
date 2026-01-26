<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'
import { useToast } from '~/composables/useToast'
const { translateLanguage } = useLanguage()

definePageMeta({
    layout: 'admin'
})

const api = useApi()
const toast = useToast()

const categories = ref<any[]>([])
const showModal = ref(false)
const isLoading = ref(false)

const form = ref({
    name: ''
})

const fetchCategories = async () => {
    try {
        const { data, error } = await api.getCategories()
        if (error.value) {
            toast.error(translateLanguage('admin.failed_load'))
            return
        }
        categories.value = data.value || []
    } catch (e) {
        console.error(e)
        toast.error(translateLanguage('admin.failed_load'))
    }
}

const handleSubmit = async () => {
    try {
        isLoading.value = true
        await api.createCategory(form.value)
        toast.success(translateLanguage('admin.save_success'))
        showModal.value = false
        form.value.name = ''
        await fetchCategories()
    } catch (e: any) {
        console.error(e)
        toast.error(e.response?._data?.detail || 'Failed to create category')
    } finally {
        isLoading.value = false
    }
}

const deleteCategory = async (id: number) => {
    if (!confirm(translateLanguage('admin.delete_confirm'))) return
    
    try {
        await api.deleteCategory(id)
        toast.success(translateLanguage('admin.delete_success'))
        await fetchCategories()
    } catch (e: any) {
        console.error(e)
        toast.error(e.response?._data?.detail || translateLanguage('admin.failed_load'))
    }
}

onMounted(() => {
    fetchCategories()
})
</script>

<template>
    <div>
        <div class="header">
            <div>
                <h1>{{ translateLanguage('admin.categories_management') }}</h1>
                <p class="subtitle">{{ translateLanguage('nav.admin_portal') }} / {{ translateLanguage('nav.categories') }}</p>
            </div>
            <button class="btn btn-primary" @click="showModal = true">+ {{ translateLanguage('admin.add_category') }}</button>
        </div>

        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>{{ translateLanguage('admin.name') }}</th>
                        <th>{{ translateLanguage('admin.actions') }}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="category in categories" :key="category.id">
                        <td>{{ category.name }}</td>
                        <td>
                            <button class="btn-icon text-danger" :title="translateLanguage('admin.delete')" @click="deleteCategory(category.id)">
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
                <h2>{{ translateLanguage('admin.add_category') }}</h2>
                <form class="form-grid" @submit.prevent="handleSubmit">
                    <div class="form-group">
                        <label>{{ translateLanguage('admin.name') }}</label>
                        <input v-model="form.name" required class="input" />
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="btn btn-outline" @click="showModal = false">{{ translateLanguage('admin.cancel') }}</button>
                        <button type="submit" class="btn btn-primary" :disabled="isLoading">
                            {{ isLoading ? translateLanguage('admin.uploading') : translateLanguage('admin.add_category') }}
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
    text-align: left;
    border-bottom: 1px solid var(--border);
}

.data-table th {
    background: #f8fafc;
    font-weight: 700;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
    border-bottom: 2px solid #e2e8f0;
}

.subtitle {
    color: var(--text-muted);
    font-size: 0.875rem;
    margin-top: 0.25rem;
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
