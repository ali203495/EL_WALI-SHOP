<script setup lang="ts">
const { init } = useSiteSettings()

// Initialize settings globally
onMounted(() => {
    init()
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
