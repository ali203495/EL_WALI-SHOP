<script setup lang="ts">
const { logout } = useAuthStore()
const route = useRoute()

const links = [
    { name: 'لوحة التحكم', path: '/account', icon: '📊' },
    { name: 'طلباتي', path: '/account/orders', icon: '🛍️' },
    { name: 'الإعدادات', path: '/account/settings', icon: '⚙️' },
]

const handleLogout = () => {
    logout()
    navigateTo('/login')
}
</script>

<template>
    <div class="account-layout" dir="rtl">
        <Nav /> <!-- Main site nav -->
        
        <div class="container account-container">
            <aside class="account-sidebar">
                <div class="sidebar-header">
                    <h3>حسابي</h3>
                </div>
                <nav class="sidebar-nav">
                    <NuxtLink 
                        v-for="link in links" 
                        :key="link.path" 
                        :to="link.path"
                        class="nav-item"
                        :class="{ active: route.path === link.path }"
                    >
                        <span class="icon">{{ link.icon }}</span>
                        {{ link.name }}
                    </NuxtLink>
                    
                    <button class="nav-item logout" @click="handleLogout">
                        <span class="icon">🚪</span>
                        تسجيل الخروج
                    </button>
                </nav>
            </aside>
            
            <main class="account-content">
                <slot />
            </main>
        </div>
        
        <Footer />
    </div>
</template>

<style scoped>
.account-layout {
    min-height: 100vh;
    background: #f8fafc;
    display: flex;
    flex-direction: column;
}

.account-container {
    flex: 1;
    display: grid;
    grid-template-columns: 250px 1fr;
    gap: 2rem;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.account-sidebar {
    background: white;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    height: fit-content;
    overflow: hidden;
}

.sidebar-header {
    padding: 1.5rem;
    background: var(--primary-light);
    border-bottom: 1px solid var(--border);
}

.sidebar-header h3 {
    margin: 0;
    color: var(--primary-hover);
    font-size: 1.25rem;
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.5rem;
    color: var(--text);
    text-decoration: none;
    transition: background 0.2s;
    border-left: 3px solid transparent;
    font-weight: 500;
}

.nav-item:hover {
    background: #f8fafc;
}

.nav-item.active {
    background: #fffbeb;
    color: var(--primary-hover);
    border-left-color: var(--primary);
}

.nav-item.logout {
    margin-top: 1rem;
    border-top: 1px solid var(--border);
    color: #ef4444;
    width: 100%;
    text-align: right;
    background: none;
    border: none;
    cursor: pointer;
    border-left: 3px solid transparent; /* Match others */
}

.nav-item.logout:hover {
    background: #fef2f2;
}

.account-content {
    background: white;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    padding: 2rem;
    min-height: 500px;
}

@media (max-width: 768px) {
    .account-container {
        grid-template-columns: 1fr;
    }
    
    .account-sidebar {
        margin-bottom: 1rem;
    }
}
</style>
