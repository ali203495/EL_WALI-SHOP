<script setup lang="ts">
import { useLanguage } from '../composables/useLanguage'

const { locale, setLocale } = useLanguage()
const isOpen = ref(false)

const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'ar', name: 'العربية', flag: '🇲🇦' }
]

const currentLanguage = computed(() => languages.find(l => l.code === locale.value))

const toggleDropdown = () => {
    isOpen.value = !isOpen.value
}

const selectLanguage = (code: string) => {
    setLocale(code as any)
    isOpen.value = false
}

// Close on click outside
if (process.client) {
    onMounted(() => {
        window.addEventListener('click', (e) => {
            if (!(e.target as HTMLElement).closest('.lang-switcher')) {
                isOpen.value = false
            }
        })
    })
}
</script>

<template>
    <div class="lang-switcher">
        <button class="lang-btn" @click="toggleDropdown" :aria-expanded="isOpen">
            <span class="flag-icon">{{ currentLanguage?.flag }}</span>
            <span class="lang-name desktop-only">{{ currentLanguage?.code.toUpperCase() }}</span>
            <span class="chevron" :class="{ rotated: isOpen }">▾</span>
        </button>
        
        <transition name="dropdown">
            <div v-if="isOpen" class="lang-dropdown">
                <button 
                    v-for="lang in languages" 
                    :key="lang.code"
                    class="lang-option"
                    :class="{ active: locale === lang.code }"
                    @click="selectLanguage(lang.code)"
                >
                    <span class="option-flag">{{ lang.flag }}</span>
                    <span class="option-name">{{ lang.name }}</span>
                    <span v-if="locale === lang.code" class="active-check">✓</span>
                </button>
            </div>
        </transition>
    </div>
</template>

<style scoped>
.lang-switcher {
    position: relative;
    z-index: 1000;
}

.lang-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: white;
    border: 1px solid var(--border);
    padding: 0.4rem 0.8rem;
    border-radius: 2rem;
    cursor: pointer;
    color: var(--text);
    font-size: 0.875rem;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.lang-btn:hover {
    border-color: var(--primary);
    background: var(--primary-light);
    transform: translateY(-1px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.flag-icon {
    font-size: 1.125rem;
}

.lang-name {
    letter-spacing: 0.05em;
    color: var(--text-muted);
}

.chevron {
    font-size: 0.75rem;
    opacity: 0.5;
    transition: transform 0.3s ease;
}

.chevron.rotated {
    transform: rotate(180deg);
}

.lang-dropdown {
    position: absolute;
    top: calc(100% + 0.75rem);
    right: 0;
    background: white;
    border: 1px solid var(--border);
    border-radius: 1rem;
    box-shadow: var(--shadow-lg);
    min-width: 170px;
    padding: 0.5rem;
    overflow: hidden;
    z-index: 1001;
}

/* RTL handling */
[dir="rtl"] .lang-dropdown {
    right: auto;
    left: 0;
}

.lang-option {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: none;
    border: none;
    cursor: pointer;
    text-align: left;
    border-radius: 0.6rem;
    transition: all 0.2s ease;
    font-size: 0.9375rem;
    color: var(--text);
}

[dir="rtl"] .lang-option {
    text-align: right;
}

.lang-option:hover {
    background: var(--primary-light);
    color: var(--primary-hover);
}

.lang-option.active {
    color: var(--primary-hover);
    background: var(--primary-light);
    font-weight: 700;
}

.option-flag {
    font-size: 1.25rem;
}

.active-check {
    margin-left: auto;
    font-size: 0.875rem;
    font-weight: 900;
}

[dir="rtl"] .active-check {
    margin-left: 0;
    margin-right: auto;
}

/* Transitions */
.dropdown-enter-active,
.dropdown-leave-active {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-enter-from,
.dropdown-leave-to {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
}

@media (max-width: 768px) {
    .lang-name.desktop-only {
        display: none;
    }
    
    .lang-btn {
        padding: 0.4rem 0.6rem;
    }
}
</style>
