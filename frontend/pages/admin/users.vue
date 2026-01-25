<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useApi } from '~/composables/useApi'
import { useToast } from '~/composables/useToast'
const { translateLanguage } = useLanguage()

definePageMeta({
    layout: 'admin'
})

const api = useApi()
const auth = useAuthStore()
const toast = useToast()

const users = ref<any[]>([])
const showModal = ref(false)
const isLoading = ref(false)

// Sudo Mode State (Removed)

const form = ref({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    password: '',
    is_admin: true,
    is_super_admin: false
})

const fetchUsers = async () => {
    try {
        const { data, error } = await api.getUsers()
        if (error.value) {
            toast.error(translateLanguage('admin.failed_load'))
            return
        }
        users.value = data.value || []
    } catch (e) {
        toast.error(translateLanguage('admin.failed_load'))
    }
}

const handleSubmit = async () => {
    try {
        isLoading.value = true
        await api.createUser(form.value)
        toast.success(translateLanguage('admin.save_success'))
        showModal.value = false
        // Reset form
        form.value = {
            username: '',
            first_name: '',
            last_name: '',
            email: '',
            phone_number: '',
            password: '',
            is_admin: true,
            is_super_admin: false
        }
        await fetchUsers()
    } catch (e: any) {
        toast.error(e.response?._data?.detail || translateLanguage('admin.save_failed'))
    } finally {
        isLoading.value = false
    }
}

const deleteUser = async (id: number) => {
    if (!confirm(translateLanguage('admin.delete_confirm'))) return
    
    try {
        await api.deleteUser(id)
        toast.success(translateLanguage('admin.delete_success'))
        await fetchUsers()
    } catch (e: any) {
        toast.error(e.response?._data?.detail || translateLanguage('admin.failed_load'))
    }
}

onMounted(() => {
    fetchUsers() 
})
</script>

<template>
    <div>
        <!-- Sudo Mode Overlay -->
        <!-- Sudo Mode Overlay Removed -->

        <div>
            <div class="header">
                <div>
                    <h1>{{ translateLanguage('admin.users_management') }}</h1>
                    <p class="subtitle">{{ translateLanguage('nav.admin_portal') }} / {{ translateLanguage('nav.users') }}</p>
                </div>
                <button v-if="auth.user?.is_super_admin" class="btn btn-primary" @click="showModal = true">+ {{ translateLanguage('admin.add_admin') }}</button>
            </div>

            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>{{ translateLanguage('admin.name') }}</th>
                            <th>{{ translateLanguage('admin.username') }}</th>
                            <th>{{ translateLanguage('admin.email') }}</th>
                            <th>{{ translateLanguage('admin.phone_number') }}</th>
                            <th>{{ translateLanguage('admin.role') }}</th>
                            <th>{{ translateLanguage('admin.status') }}</th>
                            <th>{{ translateLanguage('admin.actions') }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in users" :key="user.id">
                            <td>{{ user.first_name }} {{ user.last_name }}</td>
                            <td>{{ user.username }}</td>
                            <td>{{ user.email }}</td>
                            <td>{{ user.phone_number }}</td>
                            <td>
                                <span class="badge" :class="user.is_super_admin ? 'badge-purple' : 'badge-blue'">
                                    {{ user.is_super_admin ? translateLanguage('admin.super_admin') : translateLanguage('admin.admin') }}
                                </span>
                            </td>
                            <td>
                                <span class="badge" :class="user.is_active ? 'badge-success' : 'badge-danger'">
                                    {{ user.is_active ? translateLanguage('admin.active') : translateLanguage('admin.inactive') }}
                                </span>
                            </td>
                            <td>
                                <button class="btn-icon text-danger" :title="translateLanguage('admin.delete')" @click="deleteUser(user.id)">
                                    🗑️
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Modal for Add User -->
            <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
                <div class="modal">
                    <h2>{{ translateLanguage('admin.users_management') }}</h2>
                    <form class="form-grid" @submit.prevent="handleSubmit">
                        <div class="form-group">
                            <label>{{ translateLanguage('admin.username') }}</label>
                            <input v-model="form.username" required class="input" />
                        </div>
                        
                        <div class="form-group">
                            <label>{{ translateLanguage('admin.password') }}</label>
                            <input v-model="form.password" type="password" required class="input" />
                        </div>

                        <div class="form-group">
                            <label>{{ translateLanguage('admin.first_name') }}</label>
                            <input v-model="form.first_name" required class="input" />
                        </div>

                        <div class="form-group">
                            <label>{{ translateLanguage('admin.last_name') }}</label>
                            <input v-model="form.last_name" required class="input" />
                        </div>

                        <div class="form-group">
                            <label>{{ translateLanguage('admin.email') }}</label>
                            <input v-model="form.email" type="email" required class="input" />
                        </div>

                        <div class="form-group">
                            <label>{{ translateLanguage('admin.phone_number') }}</label>
                            <input v-model="form.phone_number" required class="input" />
                        </div>
                        
                        <div class="form-group checkbox-group">
                            <label>
                                <input v-model="form.is_super_admin" type="checkbox">
                                {{ translateLanguage('admin.set_as_super_admin') }}
                            </label>
                        </div>

                        <div class="form-actions">
                            <button type="button" class="btn btn-outline" @click="showModal = false">{{ translateLanguage('admin.cancel') }}</button>
                            <button type="submit" class="btn btn-primary" :disabled="isLoading">
                                {{ isLoading ? translateLanguage('admin.uploading') : translateLanguage('admin.add_admin') }}
                            </button>
                        </div>
                    </form>
                </div>
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
    margin-top: 1rem;
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

.badge-purple { background: #7c3aed15; color: #7c3aed; }
.badge-blue { background: #3b82f615; color: #3b82f6; }

/* Sudo Overlay */
.sudo-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: #f8fafc;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}

.sudo-box {
    background: white;
    padding: 2.5rem;
    border-radius: 1rem;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    text-align: center;
}

.sudo-box .icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.sudo-input {
    margin: 1.5rem 0;
    text-align: center;
    font-size: 1.1rem;
}

.error-text {
    color: var(--danger);
    margin-top: 0.5rem;
    font-size: 0.875rem;
}

.btn-link {
    background: none;
    border: none;
    color: #64748b;
    margin-top: 1rem;
    cursor: pointer;
    text-decoration: underline;
}

.checkbox-group {
    grid-column: span 2;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
</style>
