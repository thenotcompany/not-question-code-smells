<template>
  <div class="layout">
    <NuxtPage />
  </div>
</template>

<style>
.layout {
  position: relative;
  z-index: var(--z-content, 1);
  max-width: 880px;
  margin: 0 auto;
  padding: clamp(1rem, 3vw, 2rem) clamp(1rem, 4vw, 2.5rem) 3rem;
}
</style>
