<script setup lang="ts">
import ProjectsPanel from "~/components/ProjectsPanel.vue"
import UsersPanel from "~/components/UsersPanel.vue"

type TabId = "users" | "projects"

const activeTab = ref<TabId>("users")

function setTab(id: TabId) {
  activeTab.value = id
}
</script>

<template>
  <main class="home">
    <h1 class="home__title custom-text-hero custom-margin-zero custom-mb-2">Operations console</h1>
    <p class="home__lead custom-text-paragraph custom-tone-soft custom-mb-6 custom-max-readable">
      Users and projects in one place, backed by local API routes.
    </p>

    <div
      class="tabs custom-inline-flex custom-flex-row custom-flex-wrap custom-align-center custom-gap-2 custom-mb-5 custom-pad-3 custom-round-pill"
      role="tablist"
      aria-label="Data"
    >
      <button
        type="button"
        role="tab"
        class="tabs__btn custom-text-small custom-weight-medium"
        :class="{ 'tabs__btn--active': activeTab === 'users' }"
        :aria-selected="activeTab === 'users'"
        @click="setTab('users')"
      >
        Users
      </button>
      <button
        type="button"
        role="tab"
        class="tabs__btn custom-text-small custom-weight-medium"
        :class="{ 'tabs__btn--active': activeTab === 'projects' }"
        :aria-selected="activeTab === 'projects'"
        @click="setTab('projects')"
      >
        Projects
      </button>
    </div>

    <div class="home__body custom-round-lg custom-pad-4">
      <UsersPanel v-show="activeTab === 'users'" />
      <ProjectsPanel v-show="activeTab === 'projects'" />
    </div>
  </main>
</template>

<style scoped>
.home__title {
  color: hsl(0 0% 98%);
}

.tabs {
  background: hsl(255 28% 16% / 0.55);
  border: 1px solid hsl(255 30% 32% / 0.45);
}

.tabs__btn {
  cursor: pointer;
  border: none;
  padding: 0.5rem 1.15rem;
  border-radius: 999px;
  color: hsl(255 18% 72%);
  background: transparent;
  transition:
    color 0.2s ease,
    background 0.2s ease;
}

.tabs__btn:hover {
  color: hsl(0 0% 96%);
  background: hsl(255 30% 24% / 0.5);
}

.tabs__btn--active {
  color: hsl(168 70% 12%);
  background: linear-gradient(135deg, hsl(168 62% 58%) 0%, hsl(195 70% 52%) 100%);
  box-shadow:
    0 0 0 1px hsl(168 80% 70% / 0.35),
    0 6px 20px hsl(195 80% 40% / 0.2);
}

.home__body {
  position: relative;
  background: linear-gradient(
    160deg,
    hsl(255 26% 18% / 0.75) 0%,
    hsl(230 32% 12% / 0.65) 100%
  );
  border: 1px solid hsl(255 28% 34% / 0.55);
  box-shadow:
    0 20px 50px hsl(250 50% 4% / 0.45),
    inset 0 1px 0 0 hsl(0 0% 100% / 0.05);
}
</style>
