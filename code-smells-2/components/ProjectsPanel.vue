<script setup lang="ts">
import { useProjectList } from "~/lib/useProjectList"
import type { ProjectDto } from "~/types/api/project"

const { rows, pending, err, load: loadProjects } = useProjectList()

const projectItems = computed<ProjectDto[]>(() => rows.value?.items ?? [])

const summary = ref<{ projectCount: number; needsAttention: number } | null>(null)
const summaryPending = ref(false)
const summaryErr = ref<unknown>(null)

const detail = ref<ProjectDto | null>(null)
const detailPending = ref(false)

onMounted(async () => {
  // Load the projects
  void loadProjects()

  // We also need to load the summary of the projects
  summaryPending.value = true
  try {
    // Fetch the summary of the projects from the API
    summary.value = await $fetch<{ projectCount: number; needsAttention: number }>(
      "/api/projects/summary",
    )
  } catch (e: unknown) {
    // If there is an error, set the error state
    summaryErr.value = e
  } finally {
    // Finally, set the loading state to false
    summaryPending.value = false
  }
})
</script>

<template>
  <section class="panel custom-flex custom-flex-col" aria-labelledby="projects-heading">
    <h2 id="projects-heading" class="custom-text-section custom-tone-strong custom-margin-zero custom-mb-4">
      Projects
    </h2>

    <div v-if="summaryPending" class="custom-text-small custom-tone-muted custom-mb-3">Loading summary…</div>
    <div v-else-if="summaryErr" class="custom-text-small custom-tone-danger custom-mb-3">Summary unavailable.</div>
    <div v-else-if="summary" class="custom-text-small custom-tone-soft custom-mb-3">
      {{ summary.projectCount }} projects · {{ summary.needsAttention }} need attention
    </div>

    <div v-if="detailPending" class="custom-text-small custom-tone-muted custom-mb-3">Loading detail…</div>
    <p v-else-if="detail" class="custom-text-small custom-tone-soft custom-mb-4 custom-margin-zero">
      Detail:
      <strong class="custom-tone-strong custom-weight-bold">{{ detail.title }}</strong>
      — {{ detail.health }}
    </p>

    <div
      v-if="pending"
      class="state state--pending custom-flex custom-align-center custom-gap-3 custom-pad-4 custom-round-md"
    >
      <span class="custom-busy-ring" aria-hidden="true" />
      <span class="custom-text-small custom-weight-medium">Loading list…</span>
    </div>
    <div
      v-else-if="err"
      class="state state--err custom-flex custom-align-center custom-gap-3 custom-pad-4 custom-round-md"
    >
      <span class="custom-text-small custom-weight-medium">List failed to load.</span>
    </div>
    <div
      v-else-if="projectItems.length === 0"
      class="state custom-flex custom-align-center custom-gap-3 custom-pad-4 custom-round-md"
    >
      <span class="custom-text-small custom-weight-medium">No rows.</span>
    </div>
    <div v-else class="list custom-round-md">
      <div
        v-for="p in projectItems"
        :key="p.id"
        class="row custom-flex custom-flex-row custom-align-center custom-justify-between custom-gap-4 custom-pad-4"
      >
        <span class="row__title custom-text-paragraph custom-weight-bold custom-tone-strong">{{ p.title }}</span>
        <span class="row__health custom-text-caps-label" :data-health="p.health">{{ p.health }}</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.state {
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

.list {
  overflow: hidden;
  border: 1px solid hsl(255 26% 32% / 0.55);
  background: hsl(240 28% 10% / 0.6);
}

.row {
  border-bottom: 1px solid hsl(255 22% 22% / 0.6);
}

.row:last-child {
  border-bottom: none;
}

.row__health {
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
