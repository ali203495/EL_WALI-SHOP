<script setup lang="ts">
const api = useApi()
const { data: settingsData, error } = await api.getSettings()

// Apply theme settings
watchEffect(() => {
  if (import.meta.client && settingsData.value) {
    settingsData.value.forEach((s: any) => {
      if (s.key.startsWith('theme_')) {
        const cssVar = '--' + s.key.replace('theme_', '').replace('_', '-')
        document.documentElement.style.setProperty(cssVar, s.value)
      }
    })
  }
})
</script>

<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <ToastContainer />
  </div>
</template>
