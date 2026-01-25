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

const brands = ref<any[]>([])
const showModal = ref(false)
const isLoading = ref(false)

const form = ref({
    name: '',
    logo_url: ''
})

const fetchBrands = async () => {
    try {
        const { data, error } = await api.getBrands()
        if (error.value) {
            toast.error(translateLanguage('admin.failed_load'))
            return
        }
        brands.value = data.value || []
    } catch (e) {
        toast.error(translateLanguage('admin.failed_load'))
    }
}

const handleSubmit = async () => {
    try {
        isLoading.value = true
        await api.createBrand(form.value)
        toast.success(translateLanguage('admin.save_success'))
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
    if (!confirm(translateLanguage('admin.delete_confirm'))) return
    
    try {
        await api.deleteBrand(id)
        toast.success(translateLanguage('admin.delete_success'))
        await fetchBrands()
    } catch (e: any) {
        toast.error(e.response?._data?.detail || translateLanguage('admin.failed_load'))
    }
}

onMounted(() => {
    fetchBrands()
})
</script>

<template>
    <div>
        <div class="header">
            <div>
                <h1>{{ translateLanguage('admin.brands_management') }}</h1>
                <p class="subtitle">{{ translateLanguage('nav.admin_portal') }} / {{ translateLanguage('nav.brands') }}</p>
            </div>
            <button class="btn btn-primary" @click="showModal = true">+ {{ translateLanguage('admin.add_brand') }}</button>
        </div>

        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>{{ translateLanguage('admin.name') }}</th>
                        <th>{{ translateLanguage('admin.brand') }}</th>
                        <th>{{ translateLanguage('admin.actions') }}</th>
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
                            <button class="btn-icon text-danger" :title="translateLanguage('admin.delete')" @click="deleteBrand(brand.id)">
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
                <h2>{{ translateLanguage('admin.add_brand') }}</h2>
                <form class="form-grid" @submit.prevent="handleSubmit">
                    <div class="form-group">
                        <label>{{ translateLanguage('admin.name') }}</label>
                        <input v-model="form.name" required class="input" />
                    </div>
                     <div class="form-group">
                        <label>{{ translateLanguage('admin.logo_url') }}</label>
                        <input v-model="form.logo_url" class="input" />
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="btn btn-outline" @click="showModal = false">{{ translateLanguage('admin.cancel') }}</button>
                        <button type="submit" class="btn btn-primary" :disabled="isLoading">
                            {{ isLoading ? translateLanguage('admin.uploading') : translateLanguage('admin.add_brand') }}
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
