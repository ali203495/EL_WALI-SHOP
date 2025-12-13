<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const auth = useAuthStore()
</script>

<template>
    <div class="admin-layout" dir="rtl">
        <nav class="sidebar">
            <div class="logo">
                <h2>EL WALI<span>.ADMIN</span></h2>
            </div>
            <ul class="nav-menu">
                <li>
                    <NuxtLink to="/admin" exact-active-class="active">
                        <span class="icon">📊</span> لوحة التحكم
                    </NuxtLink>
                </li>
                <li>
                    <NuxtLink to="/admin/products" active-class="active">
                        <span class="icon">📦</span> المنتجات
                    </NuxtLink>
                </li>
                <li>
                    <NuxtLink to="/admin/orders" active-class="active">
                        <span class="icon">🧾</span> الطلبات
                    </NuxtLink>
                </li>
                 <li>
                    <NuxtLink to="/admin/users" active-class="active">
                        <span class="icon">👥</span> المستخدمين
                    </NuxtLink>
                </li>
                <li>
                    <NuxtLink to="/admin/settings" active-class="active">
                        <span class="icon">⚙️</span> الإعدادات
                    </NuxtLink>
                </li>
                 <li>
                    <NuxtLink to="/admin/categories" active-class="active">
                        <span class="icon">📂</span> الفئات
                    </NuxtLink>
                </li>
                 <li>
                    <NuxtLink to="/admin/brands" active-class="active">
                        <span class="icon">🏷️</span> الماركات
                    </NuxtLink>
                </li>
                 <li>
                    <NuxtLink to="/admin/stores" active-class="active">
                        <span class="icon">🏪</span> المتاجر
                    </NuxtLink>
                </li>
                <li>
                    <NuxtLink to="/pos" active-class="active">
                        <span class="icon">💳</span> نقطة البيع
                    </NuxtLink>
                </li>
            </ul>
            <div class="sidebar-footer">
                <NuxtLink to="/" class="back-link">← العودة للمتجر</NuxtLink>
            </div>
        </nav>
        
        <main class="content">
            <slot />
        </main>
    </div>
</template>

<style scoped>
.admin-layout {
    display: grid;
    grid-template-columns: 260px 1fr;
    min-height: 100vh;
    background: #f1f5f9;
}

.sidebar {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    color: white;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 0;
    height: 100vh;
}

.logo h2 {
    font-size: 1.5rem;
    font-weight: 800;
}

.logo span {
    color: var(--primary);
}

.nav-menu {
    list-style: none;
    margin-top: 3rem;
    flex: 1;
}

.nav-menu li {
    margin-bottom: 0.5rem;
}

.nav-menu a {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.875rem 1rem;
    color: #94a3b8;
    text-decoration: none;
    border-radius: 0.5rem;
    transition: all 0.2s;
}

.nav-menu a:hover,
.nav-menu a.active {
    background: rgba(255,255,255,0.1);
    color: white;
}

.icon {
    font-size: 1.25rem;
}

.sidebar-footer {
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 1rem;
}

.back-link {
    color: #64748b;
    text-decoration: none;
    font-size: 0.875rem;
}

.content {
    padding: 2rem 3rem;
    overflow-y: auto;
}
</style>
