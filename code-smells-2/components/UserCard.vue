<script setup lang="ts">
import type { UserDto } from "~/types/api/user"

defineProps<{ user: UserDto }>()
</script>

<template>
  <!-- card for a single user -->
  <article
    class="card custom-flex custom-flex-row custom-flex-wrap custom-align-baseline custom-gap-3 custom-pad-4 custom-round-md">
    <!-- user's display name -->
    <strong class="card__name custom-text-subsection custom-tone-strong">{{ user.name }}</strong>
    <!-- user's id string -->
    <span class="card__id custom-text-fine custom-tone-soft custom-text-caps custom-weight-medium">{{ user.id }}</span>
  </article>
</template>

<style scoped>
.card {
  position: relative;
  overflow: hidden;
  background: linear-gradient(125deg,
      hsl(255 26% 20% / 0.92) 0%,
      hsl(232 30% 16% / 0.88) 55%,
      hsl(255 22% 18% / 0.75) 100%);
  border: 1px solid hsl(255 32% 36% / 0.45);
  box-shadow:
    0 2px 4px hsl(0 0% 0% / 0.2),
    0 12px 32px hsl(250 45% 6% / 0.35),
    inset 0 1px 0 0 hsl(0 0% 100% / 0.05);
  transition:
    transform var(--dur, 220ms) var(--ease-out, ease),
    box-shadow var(--dur, 220ms) var(--ease-out, ease),
    border-color var(--dur, 220ms) var(--ease-out, ease);
}

.card::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  border-radius: 4px 0 0 4px;
  background: linear-gradient(180deg, hsl(168 65% 52%) 0%, hsl(252 70% 62%) 100%);
}

.card:hover {
  transform: translateY(-2px);
  border-color: hsl(168 40% 42% / 0.55);
  box-shadow:
    0 4px 8px hsl(0 0% 0% / 0.25),
    0 18px 40px hsl(250 50% 5% / 0.45),
    inset 0 1px 0 0 hsl(0 0% 100% / 0.07);
}

.card__id {
  font-variant-numeric: tabular-nums;
  letter-spacing: 0.04em;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  background: hsl(255 22% 14% / 0.9);
  border: 1px solid hsl(255 25% 28% / 0.5);
}
</style>
