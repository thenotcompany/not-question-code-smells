<script setup lang="ts">
import { useProjectList } from "~/misc/useProjectList"
import MetricTile from "./partials/MetricTile.vue"
import type { ProjectDto } from "~/types/api/project"

const { rows, pending, err, load } = useProjectList()

const projectItems = computed<ProjectDto[]>(() => rows.value?.items ?? [])

onMounted(async () => {
  await load()
})
</script>

<template>
  <!-- dashboard route -->
  <main class="page">
    <h2>Dashboard</h2>
    <div v-if="pending" class="state state--pending">
      <span class="spinner" aria-hidden="true" />
      Loading…
    </div>
    <div v-else-if="err" class="state state--err">
      Something went wrong.
    </div>
    <div v-else-if="projectItems.length === 0" class="state">No rows.</div>
    <div v-else class="grid">
      <MetricTile title="Projects" :value="projectItems.length" />
      <div class="list">
        <div v-for="p in projectItems" :key="p.id" class="row">
          <span class="row__title">{{ p.title }}</span>
          <span class="row__health" :data-health="p.health">{{ p.health }}</span>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.page {
  position: relative;
}

.state {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 1rem 1.2rem;
  border-radius: var(--r-md, 16px);
  font-weight: 500;
  color: hsl(255 12% 82%);
  background: hsl(255 22% 14% / 0.65);
  border: 1px solid hsl(255 25% 30% / 0.55);
}

.state--pending {
  border-color: hsl(252 35% 36% / 0.6);
}

.state--err {
  color: hsl(355 85% 88%);
  border-color: hsl(355 55% 42% / 0.65);
  background: linear-gradient(
    135deg,
    hsl(355 40% 18% / 0.85) 0%,
    hsl(255 25% 14% / 0.75) 100%
  );
}

.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid hsl(255 20% 32%);
  border-top-color: hsl(168 62% 55%);
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.grid {
  display: grid;
  grid-template-columns: minmax(200px, 280px) 1fr;
  gap: clamp(1rem, 3vw, 1.75rem);
  align-items: start;
}

@media (max-width: 640px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

.list {
  border-radius: var(--r-md, 16px);
  overflow: hidden;
  border: 1px solid hsl(255 26% 32% / 0.55);
  background: hsl(240 28% 10% / 0.6);
  box-shadow: inset 0 0 0 1px hsl(0 0% 100% / 0.03);
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem 1.1rem;
  border-bottom: 1px solid hsl(255 22% 22% / 0.6);
  transition: background var(--dur, 220ms) var(--ease-out, ease);
}

.row:last-child {
  border-bottom: none;
}

.row:hover {
  background: hsl(255 24% 16% / 0.5);
}

.row__title {
  font-weight: 600;
  color: hsl(0 0% 94%);
}

.row__health {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0.35rem 0.65rem;
  border-radius: 999px;
  border: 1px solid hsl(255 25% 35% / 0.6);
}

.row__health[data-health="ok"] {
  color: hsl(155 70% 42%);
  border-color: hsl(155 50% 32% / 0.7);
  background: hsl(155 40% 14% / 0.55);
}

.row__health[data-health="warn"] {
  color: hsl(38 92% 58%);
  border-color: hsl(38 60% 36% / 0.7);
  background: hsl(38 45% 16% / 0.55);
}
</style>
