<script setup lang="ts">
import { ref } from 'vue'

const mobileMenuOpen = ref(false)
const searchOpen = ref(false)
const searchQuery = ref('')
const cartDrawerOpen = ref(false)

const { isDark, toggle: toggleDarkMode } = useDarkMode()
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
    <!-- Header -->
    <header class="navbar">
      <div class="container nav-content">
        <NuxtLink to="/" class="logo">
          <span v-if="settings.store_name">{{ settings.store_name }}</span>
          <span v-else>MAISON <span class="highlight">EL WALI</span></span>
        </NuxtLink>
        
        <nav class="nav-links desktop-only">
          <NuxtLink to="/catalog">Collections</NuxtLink>
          <NuxtLink to="/packages">Packages</NuxtLink>
          <NuxtLink to="/boutique">Boutique</NuxtLink>
          <NuxtLink to="/about">The Maison</NuxtLink>
          <NuxtLink to="/contact">Concierge</NuxtLink>
        </nav>
        
        <div class="nav-actions">
          <button class="icon-btn" @click="searchOpen = !searchOpen" title="Search">
            🔍
          </button>
          
          <button class="icon-btn cart-btn" @click="cartDrawerOpen = true" title="Cart">
            <span class="cart-icon">🛒</span>
            <span v-if="itemCount > 0" class="cart-badge">{{ itemCount }}</span>
          </button>

          <button class="icon-btn" @click="toggleDarkMode" :title="isDark ? 'Light Mode' : 'Dark Mode'">
            {{ isDark ? '☀️' : '🌙' }}
          </button>
          
          <NuxtLink to="/login" class="btn btn-sm btn-primary desktop-only">
            login
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
            placeholder="Search products..." 
            class="search-input" 
            autofocus
          >
          <button type="submit" class="btn btn-primary">Search</button>
        </form>
      </div>
      
      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="mobile-menu">
        <nav>
          <NuxtLink to="/catalog" @click="mobileMenuOpen = false">Collections</NuxtLink>
          <NuxtLink to="/packages" @click="mobileMenuOpen = false">Packages</NuxtLink>
          <NuxtLink to="/boutique" @click="mobileMenuOpen = false">Boutique</NuxtLink>
          <NuxtLink to="/about" @click="mobileMenuOpen = false">About</NuxtLink>
          <NuxtLink to="/contact" @click="mobileMenuOpen = false">Contact</NuxtLink>
          <NuxtLink to="/login" @click="mobileMenuOpen = false">Admin Portal</NuxtLink>
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
            <p>Luxury Gold & Jewelry</p>
            <p class="tagline">Timeless Elegance from Dubai</p>
            <div class="social-links">
              <a v-if="settings.contact_email" :href="'mailto:' + settings.contact_email" title="Email">✉️</a>
              <a href="#" title="Instagram">📷</a>
              <a href="#" title="Facebook">f</a>
            </div>
          </div>
          
          <!-- Shop Links -->
          <div class="footer-section">
            <h4>Collections</h4>
            <ul>
              <li><NuxtLink to="/catalog">All Jewelry</NuxtLink></li>
              <li><NuxtLink to="/catalog">Gold Rings</NuxtLink></li>
              <li><NuxtLink to="/catalog">Diamond Necklaces</NuxtLink></li>
              <li><NuxtLink to="/catalog">Luxury Watches</NuxtLink></li>
              <li><NuxtLink to="/catalog">Bridal Set</NuxtLink></li>
            </ul>
          </div>
          
          <!-- Company Links -->
          <div class="footer-section">
            <h4>The Maison</h4>
            <ul>
              <li><NuxtLink to="/boutique">Our Boutique</NuxtLink></li>
              <li><NuxtLink to="/about">Heritage</NuxtLink></li>
              <li><NuxtLink to="/contact">Careers</NuxtLink></li>
              <li><NuxtLink to="/contact">Concierge</NuxtLink></li>
            </ul>
          </div>
          
          <!-- Support Links -->
          <div class="footer-section">
            <h4>Client Care</h4>
            <ul>
              <li><NuxtLink to="/contact">Book Appt.</NuxtLink></li>
              <li><NuxtLink to="/about">Shipping & Returns</NuxtLink></li>
              <li><NuxtLink to="/about">Size Guide</NuxtLink></li>
              <li><NuxtLink to="/about">Jewelry Care</NuxtLink></li>
            </ul>
          </div>
        </div>
        
        <div class="footer-bottom">
            <p class="address">{{ settings.contact_address }}</p>
          <p class="copyright">© 2025 Maison El Wali. All Rights Reserved.</p>
        </div>
      </div>
    </footer>
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
</style>
