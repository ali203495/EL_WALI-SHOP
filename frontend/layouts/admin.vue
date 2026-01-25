<script setup lang="ts">
import { useLanguage } from '../composables/useLanguage'

const { translateLanguage } = useLanguage()
</script>

<template>
    <div class="admin-layout">
        <nav class="sidebar">
            <div class="logo">
                <h2>MAISON EL WALI <span>ARTISAN PORTAL</span></h2>
            </div>
            <ul class="nav-menu">
                <li>
                    <NuxtLink to="/admin" exact-active-class="active">
                        <span class="icon">🏛️</span> {{ translateLanguage('nav.admin_portal') }}
                    </NuxtLink>
                </li>
                <li>
                    <NuxtLink to="/admin/products" active-class="active">
                        <span class="icon">✨</span> {{ translateLanguage('nav.products') || 'Creations' }}
                    </NuxtLink>
                </li>
                <li>
                    <NuxtLink to="/admin/orders" active-class="active">
                        <span class="icon">📜</span> {{ translateLanguage('nav.orders') || 'Treasure History' }}
                    </NuxtLink>
                </li>
                 <li>
                    <NuxtLink to="/admin/users" active-class="active">
                        <span class="icon">👑</span> {{ translateLanguage('nav.users') || 'Users' }}
                    </NuxtLink>
                </li>
                <li>
                    <NuxtLink to="/admin/settings" active-class="active">
                        <span class="icon">⚜️</span> {{ translateLanguage('nav.settings') || 'Settings' }}
                    </NuxtLink>
                </li>
                 <li>
                    <NuxtLink to="/admin/categories" active-class="active">
                        <span class="icon">🏺</span> {{ translateLanguage('nav.categories') || 'Curations' }}
                    </NuxtLink>
                </li>
                 <li>
                    <NuxtLink to="/admin/brands" active-class="active">
                        <span class="icon">⚒️</span> {{ translateLanguage('nav.brands') || 'Artisans' }}
                    </NuxtLink>
                </li>
                 <li>
                    <NuxtLink to="/admin/stores" active-class="active">
                        <span class="icon">💎</span> {{ translateLanguage('nav.stores') || 'Boutiques' }}
                    </NuxtLink>
                </li>
                <li>
                    <NuxtLink to="/pos" active-class="active">
                        <span class="icon">💸</span> {{ translateLanguage('nav.pos') || 'POS' }}
                    </NuxtLink>
                </li>
            </ul>
             <div class="sidebar-footer">
                <LanguageSwitcher class="mb-4" />
                <div class="view-site-links">
                    <NuxtLink to="/" class="back-link">
                        <span class="link-icon">🏠</span> 
                        {{ translateLanguage('common.back_to_store') }}
                    </NuxtLink>
                    <NuxtLink to="/catalog" class="back-link">
                        <span class="link-icon">🛍️</span> 
                        {{ translateLanguage('nav.catalog') || 'Collections' }}
                    </NuxtLink>
                    <NuxtLink to="/boutique" class="back-link">
                        <span class="link-icon">🏢</span> 
                        {{ translateLanguage('nav.boutique') || 'Boutique' }}
                    </NuxtLink>
                </div>
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
    grid-template-columns: 280px 1fr;
    min-height: 100vh;
    background: #f8fafc;
}

.sidebar {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    color: white;
    padding: 2.5rem 1.5rem;
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 0;
    height: 100vh;
    box-shadow: 4px 0 24px rgba(0,0,0,0.1);
}

.logo {
    margin-bottom: 3rem;
    padding: 0 1rem;
}

.logo h2 {
    font-family: 'Inter', sans-serif;
    font-size: 1.125rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: white;
}

.logo span {
    display: block;
    font-size: 0.65rem;
    font-weight: 500;
    color: var(--primary);
    opacity: 0.8;
    margin-top: 0.25rem;
}

.nav-menu {
    list-style: none;
    flex: 1;
}

.nav-menu li {
    margin-bottom: 0.25rem;
}

.nav-menu a {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1rem;
    color: #94a3b8;
    text-decoration: none;
    border-radius: 0.75rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 0.9375rem;
    font-weight: 500;
}

.nav-menu a:hover {
    color: white;
    background: rgba(255, 255, 255, 0.05);
}

.nav-menu a.active {
    background: var(--primary);
    color: white;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
}

.nav-menu a.active .icon {
    transform: scale(1.1);
}

.icon {
    font-size: 1.125rem;
    transition: transform 0.3s;
}

.sidebar-footer {
    border-top: 1px solid rgba(255,255,255,0.08);
    padding-top: 1.5rem;
}

.view-site-links {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.back-link {
    color: #64748b;
    text-decoration: none;
    font-size: 0.8125rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    transition: all 0.2s;
    font-weight: 500;
}

.back-link:hover {
    color: white;
    background: rgba(255, 255, 255, 0.05);
}

.link-icon {
    font-size: 1rem;
    opacity: 0.7;
}

.content {
    padding: 2.5rem 3.5rem;
    overflow-y: auto;
}
</style>
