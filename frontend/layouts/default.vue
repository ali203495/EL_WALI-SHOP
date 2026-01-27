<script setup lang="ts">
import { ref } from 'vue'
import { useLanguage } from '../composables/useLanguage'

const mobileMenuOpen = ref(false)
const searchOpen = ref(false)
const searchQuery = ref('')
const cartDrawerOpen = ref(false)

const { translateLanguage } = useLanguage()
const { itemCount } = useCart()

const toggleMobileMenu = () => {
    mobileMenuOpen.value = !mobileMenuOpen.value
}

const handleSearch = () => {
    if (searchQuery.value.trim()) {
        navigateTo({ path: '/search', query: { q: searchQuery.value } })
        searchOpen.value = false
        searchQuery.value = ''
    }
}

const { settings } = useSiteSettings();
</script>

<template>
  <div class="public-layout">
    <AdminBar />
    <!-- Header -->
    <header class="navbar">
      <div class="container nav-content">
        <NuxtLink to="/" class="logo">
          <span v-if="settings.store_name">{{ settings.store_name }}</span>
          <span v-else>MAISON <span class="highlight">EL WALI</span></span>
        </NuxtLink>
        
        <nav class="nav-links desktop-only">
          <NuxtLink to="/catalog">{{ translateLanguage('nav.catalog') }}</NuxtLink>
          <NuxtLink to="/packages">{{ translateLanguage('nav.packages') }}</NuxtLink>
          <NuxtLink to="/boutique">{{ translateLanguage('nav.boutique') }}</NuxtLink>
          <NuxtLink to="/about">{{ translateLanguage('nav.about') }}</NuxtLink>
          <NuxtLink to="/contact">{{ translateLanguage('nav.contact') }}</NuxtLink>
        </nav>
        
        <div class="nav-actions">
          <button class="icon-btn" title="Search" @click="searchOpen = !searchOpen">
            🔍
          </button>
          
          <button class="icon-btn cart-btn" :title="translateLanguage('common.cart')" @click="cartDrawerOpen = true">
            <span class="cart-icon">🛒</span>
            <span v-if="itemCount > 0" class="cart-badge">{{ itemCount }}</span>
          </button>

          <LanguageSwitcher />
          
          <NuxtLink to="/login" class="btn btn-sm btn-primary desktop-only">
            {{ translateLanguage('nav.login') }}
          </NuxtLink>
          
          <button class="icon-btn mobile-only" @click="toggleMobileMenu">
            <span v-if="!mobileMenuOpen">☰</span>
            <span v-else>✕</span>
          </button>
        </div>
      </div>
      
      <!-- Search Bar -->
      <div v-if="searchOpen" class="search-bar">
        <form class="container" @submit.prevent="handleSearch">
          <input 
            v-model="searchQuery"
            type="text" 
            :placeholder="translateLanguage('common.search')" 
            class="search-input" 
            autofocus
          >
          <button type="submit" class="btn btn-primary">{{ translateLanguage('common.search_btn') }}</button>
        </form>
      </div>
      
      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="mobile-menu">
        <div class="mobile-lang-switcher">
           <LanguageSwitcher />
        </div>
        <nav>
          <NuxtLink to="/catalog" @click="mobileMenuOpen = false">{{ translateLanguage('nav.catalog') }}</NuxtLink>
          <NuxtLink to="/packages" @click="mobileMenuOpen = false">{{ translateLanguage('nav.packages') }}</NuxtLink>
          <NuxtLink to="/boutique" @click="mobileMenuOpen = false">{{ translateLanguage('nav.boutique') }}</NuxtLink>
          <NuxtLink to="/about" @click="mobileMenuOpen = false">{{ translateLanguage('nav.about') }}</NuxtLink>
          <NuxtLink to="/contact" @click="mobileMenuOpen = false">{{ translateLanguage('nav.contact') }}</NuxtLink>
          <NuxtLink to="/login" @click="mobileMenuOpen = false">{{ translateLanguage('nav.admin_portal') }}</NuxtLink>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main>
      <slot />
    </main>

    <!-- Cart Drawer -->
    <CartDrawer :is-open="cartDrawerOpen" @close="cartDrawerOpen = false" />

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-grid">
          <!-- Brand -->
          <div class="footer-brand">
            <h3><span v-if="settings.store_name">{{ settings.store_name }}</span><span v-else>MAISON <span class="highlight">EL WALI</span></span></h3>
            <p>{{ translateLanguage('footer.luxury') }}</p>
            <p class="tagline">{{ translateLanguage('footer.tagline') }}</p>
            <div class="social-links">
              <a v-if="settings.contact_email" :href="'mailto:' + settings.contact_email" title="Email">✉️</a>
              <a href="#" title="Instagram">📷</a>
              <a href="#" title="Facebook">f</a>
            </div>
          </div>
          
          <!-- Shop Links -->
          <div class="footer-section">
            <h4>{{ translateLanguage('footer.collections') }}</h4>
            <ul>
              <li><NuxtLink to="/catalog">{{ translateLanguage('footer.all_jewelry') }}</NuxtLink></li>
              <li><NuxtLink to="/catalog">{{ translateLanguage('footer.gold_rings') }}</NuxtLink></li>
              <li><NuxtLink to="/catalog">{{ translateLanguage('footer.diamond_necklaces') }}</NuxtLink></li>
              <li><NuxtLink to="/catalog">{{ translateLanguage('footer.luxury_watches') }}</NuxtLink></li>
              <li><NuxtLink to="/catalog">{{ translateLanguage('footer.bridal_set') }}</NuxtLink></li>
            </ul>
          </div>
          
          <!-- Company Links -->
          <div class="footer-section">
            <h4>{{ translateLanguage('footer.maison') }}</h4>
            <ul>
              <li><NuxtLink to="/boutique">{{ translateLanguage('nav.boutique') }}</NuxtLink></li>
              <li><NuxtLink to="/about">{{ translateLanguage('footer.heritage') }}</NuxtLink></li>
              <li><NuxtLink to="/contact">{{ translateLanguage('footer.careers') }}</NuxtLink></li>
              <li><NuxtLink to="/contact">{{ translateLanguage('nav.contact') }}</NuxtLink></li>
            </ul>
          </div>
          
          <!-- Support Links -->
          <div class="footer-section">
            <h4>{{ translateLanguage('footer.client_care') }}</h4>
            <ul>
              <li><NuxtLink to="/contact">{{ translateLanguage('footer.book_appt') }}</NuxtLink></li>
              <li><NuxtLink to="/about">{{ translateLanguage('footer.shipping_returns') }}</NuxtLink></li>
              <li><NuxtLink to="/about">{{ translateLanguage('footer.size_guide') }}</NuxtLink></li>
              <li><NuxtLink to="/about">{{ translateLanguage('footer.jewelry_care') }}</NuxtLink></li>
            </ul>
          </div>
        </div>
        
        <div class="footer-bottom">
            <p class="address">{{ settings.contact_address }}</p>
          <p class="copyright">© 2025 Maison El Wali. {{ translateLanguage('footer.rights') }}</p>
        </div>
      </div>
    </footer>

    <!-- Floating WhatsApp Button -->
    <a 
        v-if="settings.whatsapp_number" 
        :href="`https://wa.me/${settings.whatsapp_number}`" 
        target="_blank" 
        class="whatsapp-float"
        title="Chat on WhatsApp"
    >
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="white">
            <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
        </svg>
    </a>
  </div>
</template>

<style scoped>
/* Navbar */
.navbar {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(0,0,0,0.05);
}

.nav-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
}

.logo {
    font-size: 1.5rem;
    font-weight: 800;
    text-decoration: none;
    color: var(--text);
    letter-spacing: -0.5px;
}

.highlight {
    color: var(--primary);
}

.nav-links {
    display: flex;
    gap: 2.5rem;
}

.nav-links a {
    text-decoration: none;
    color: var(--text-muted);
    font-weight: 500;
    font-size: 0.9375rem;
    transition: color 0.2s;
    position: relative;
}

.nav-links a:hover,
.nav-links a.router-link-active {
    color: var(--primary);
}

.nav-links a.router-link-active::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--primary);
    border-radius: 1px;
}

.nav-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.icon-btn {
    background: none;
    border: none;
    font-size: 1.25rem;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    transition: background 0.2s;
    position: relative;
}

.icon-btn:hover {
    background: #f1f5f9;
}

.cart-btn {
    position: relative;
}

.cart-badge {
    position: absolute;
    top: -2px;
    right: -2px;
    background: #ef4444;
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid white;
}

/* Search Bar */
.search-bar {
    padding: 1rem 0;
    border-top: 1px solid var(--border);
    background: var(--surface);
}

.search-bar .container {
    display: flex;
    gap: 1rem;
}

.search-input {
    flex: 1;
    padding: 0.75rem 1.25rem;
    border: 2px solid var(--border);
    border-radius: var(--radius);
    font-size: 1rem;
}

.search-input:focus {
    outline: none;
    border-color: var(--primary);
}

/* Mobile Menu */
.mobile-menu {
    padding: 1rem;
    background: var(--surface);
    border-top: 1px solid var(--border);
}

.mobile-lang-switcher {
    margin-bottom: 1rem;
    display: flex;
    justify-content: flex-end;
}

.mobile-menu nav {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.mobile-menu a {
    padding: 1rem;
    text-decoration: none;
    color: var(--text);
    font-weight: 500;
    border-radius: var(--radius);
}

.mobile-menu a:hover {
    background: #f1f5f9;
}

/* Footer */
.footer {
    background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
    color: white;
    padding: 5rem 0 2rem;
    margin-top: 0;
}

.footer-grid {
    display: grid;
    grid-template-columns: 2fr repeat(3, 1fr);
    gap: 4rem;
    margin-bottom: 4rem;
}

.footer-brand h3 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.footer-brand p {
    color: #94a3b8;
    margin-bottom: 0.25rem;
}

.tagline {
    font-style: italic;
    font-size: 0.875rem;
}

.social-links {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
}

.social-links a {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.1);
    border-radius: 50%;
    text-decoration: none;
    font-size: 1.25rem;
    transition: background 0.2s;
}

.social-links a:hover {
    background: var(--primary);
}

.footer-section h4 {
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1.5rem;
    color: white;
}

.footer-section ul {
    list-style: none;
}

.footer-section li {
    margin-bottom: 0.75rem;
}

.footer-section a {
    color: #94a3b8;
    text-decoration: none;
    font-size: 0.9375rem;
    transition: color 0.2s;
}

.footer-section a:hover {
    color: white;
}

.footer-bottom {
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 2rem;
    text-align: center;
}

.copyright {
    color: #64748b;
    margin-bottom: 0.5rem;
}

.legal {
    font-size: 0.75rem;
    color: #475569;
}

/* Responsive */
.mobile-only {
    display: none;
}

@media (max-width: 768px) {
    .desktop-only {
        display: none;
    }
    
    .mobile-only {
        display: block;
    }
    
    .footer-grid {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
}

.whatsapp-float {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    width: 60px;
    height: 60px;
    background-color: #25d366;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1000;
    transition: all 0.3s;
    text-decoration: none;
}

.whatsapp-float:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    background-color: #22bf5b;
}
</style>
