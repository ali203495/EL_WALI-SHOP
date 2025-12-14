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
        const { data } = await api.getUsers()
        users.value = data.value || []
    } catch (e) {
        toast.error('Failed to fetch users')
    }
}

const handleSubmit = async () => {
    try {
        isLoading.value = true
        await api.createUser(form.value)
        toast.success('Admin added successfully')
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
        toast.error(e.response?._data?.detail || 'Failed to create admin')
    } finally {
        isLoading.value = false
    }
}

const deleteUser = async (id: number) => {
    if (!confirm('Are you sure you want to delete this user?')) return
    
    try {
        await api.deleteUser(id)
        toast.success('User deleted')
        await fetchUsers()
    } catch (e: any) {
        toast.error(e.response?._data?.detail || 'Failed to delete user')
    }
}

onMounted(() => {
    fetchUsers() 
})
</script>

<template>
    <div dir="rtl">
        <!-- Sudo Mode Overlay -->
        <!-- Sudo Mode Overlay Removed -->

        <div>
            <div class="header">
                <h1>إدارة المسؤولين</h1>
                <button v-if="auth.user?.is_super_admin" @click="showModal = true" class="btn btn-primary">+ إضافة مسؤول</button>
            </div>

            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>الاسم</th>
                            <th>اسم المستخدم</th>
                            <th>البريد الإلكتروني</th>
                            <th>رقم الهاتف</th>
                            <th>الصلاحية</th>
                            <th>الحالة</th>
                            <th>إجراءات</th>
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
                                    {{ user.is_super_admin ? 'مسؤول ممتاز' : 'مسؤول' }}
                                </span>
                            </td>
                            <td>
                                <span class="badge" :class="user.is_active ? 'badge-success' : 'badge-danger'">
                                    {{ user.is_active ? 'نشط' : 'غير نشط' }}
                                </span>
                            </td>
                            <td>
                                <button @click="deleteUser(user.id)" class="btn-icon text-danger" title="حذف">
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
                    <h2>إضافة مسؤول جديد</h2>
                    <form @submit.prevent="handleSubmit" class="form-grid">
                        <div class="form-group">
                            <label>اسم المستخدم</label>
                            <input v-model="form.username" required class="input" />
                        </div>
                        
                        <div class="form-group">
                            <label>كلمة المرور</label>
                            <input v-model="form.password" type="password" required class="input" />
                        </div>

                        <div class="form-group">
                            <label>الاسم الأول</label>
                            <input v-model="form.first_name" required class="input" />
                        </div>

                        <div class="form-group">
                            <label>الاسم العائلة</label>
                            <input v-model="form.last_name" required class="input" />
                        </div>

                        <div class="form-group">
                            <label>البريد الإلكتروني</label>
                            <input v-model="form.email" type="email" required class="input" />
                        </div>

                        <div class="form-group">
                            <label>رقم الهاتف</label>
                            <input v-model="form.phone_number" required class="input" />
                        </div>
                        
                        <div class="form-group checkbox-group">
                            <label>
                                <input type="checkbox" v-model="form.is_super_admin">
                                تعيين كمسؤول ممتاز (Super Admin)
                            </label>
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
