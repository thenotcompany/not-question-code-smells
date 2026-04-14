<script setup lang="ts">
defineProps<{
  title: string
  value: string | number
}>()
</script>

<template>
  <!-- metric block -->
  <div class="tile">
    <!-- label line -->
    <div class="tile__label">{{ title }}</div>
    <!-- numeric or text value -->
    <div class="tile__value">{{ value }}</div>
  </div>
</template>

<style scoped>
.tile {
  position: relative;
  padding: 1.25rem 1.35rem;
  border-radius: var(--r-md, 16px);
  background:
    radial-gradient(120% 80% at 10% 0%, hsl(168 45% 38% / 0.22), transparent 55%),
    linear-gradient(145deg, hsl(255 28% 22% / 0.95) 0%, hsl(235 32% 14% / 0.9) 100%);
  border: 1px solid hsl(255 30% 38% / 0.5);
  box-shadow:
    inset 0 1px 0 0 hsl(0 0% 100% / 0.06),
    0 10px 36px hsl(245 45% 5% / 0.4);
}

.tile::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  opacity: 0.35;
  background: linear-gradient(
    105deg,
    transparent 40%,
    hsl(0 0% 100% / 0.04) 50%,
    transparent 60%
  );
}

.tile__label {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: hsl(255 18% 58%);
  margin-bottom: 0.45rem;
}

.tile__value {
  font-size: clamp(1.75rem, 4vw, 2.35rem);
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1;
  background: linear-gradient(100deg, hsl(0 0% 100%) 0%, hsl(168 55% 72%) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
</style>
