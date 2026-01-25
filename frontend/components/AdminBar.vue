<script setup lang="ts">
const auth = useAuthStore()
const { translateLanguage } = useLanguage()

const isAdmin = computed(() => auth.user?.is_admin || auth.user?.is_super_admin)

const handleLogout = () => {
    auth.logout()
}
</script>

<template>
    <div v-if="isAdmin" class="admin-bar">
        <div class="container bar-content">
            <div class="bar-left">
                <span class="admin-badge">ARTISAN</span>
                <NuxtLink to="/admin" class="bar-link">
                    📊 {{ translateLanguage('admin.dashboard') }}
                </NuxtLink>
                <NuxtLink to="/pos" class="bar-link">
                    💳 {{ translateLanguage('nav.pos') }}
                </NuxtLink>
            </div>
            <div class="bar-right">
                <span v-if="auth.user" class="user-info">
                    👤 {{ auth.user.username }}
                </span>
                <button @click="handleLogout" class="logout-btn">
                    {{ translateLanguage('common.logout') || 'Logout' }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.admin-bar {
    background: #0f172a;
    color: white;
    padding: 0.5rem 0;
    font-size: 0.8125rem;
    z-index: 1001;
    position: sticky;
    top: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.bar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.bar-left, .bar-right {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.admin-badge {
    background: var(--primary);
    color: white;
    padding: 0.125rem 0.5rem;
    border-radius: 4px;
    font-weight: 800;
    font-size: 0.7rem;
}

.bar-link {
    color: #94a3b8;
    text-decoration: none;
    transition: color 0.2s;
    font-weight: 500;
}

.bar-link:hover {
    color: white;
}

.user-info {
    color: #94a3b8;
}

.logout-btn {
    background: none;
    border: none;
    color: #ef4444;
    cursor: pointer;
    font-size: 0.8125rem;
    font-weight: 500;
    padding: 0;
}

.logout-btn:hover {
    text-decoration: underline;
}

@media (max-width: 768px) {
    .user-info {
        display: none;
    }
    .bar-left, .bar-right {
        gap: 1rem;
    }
}
</style>
