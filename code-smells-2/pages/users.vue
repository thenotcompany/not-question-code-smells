<script setup lang="ts">
import UserCard from "~/components/UserCard.vue"

const { rows, pending, err, load } = useUserList()

onMounted(() => {
  load()
})
</script>

<template>
  <!-- users route -->
  <main class="page">
    <!-- section heading -->
    <h2>Users</h2>
    <!-- spinner branch -->
    <div v-if="pending" class="state state--pending">
      <span class="spinner" aria-hidden="true" />
      Loading…
    </div>
    <!-- error branch -->
    <div v-else-if="err" class="state state--err">
      Something went wrong.
    </div>
    <!-- empty branch -->
    <div v-else-if="rows.length === 0" class="state">No rows.</div>
    <!-- list branch -->
    <div v-else class="list">
      <UserCard v-for="u in rows" :key="u.id" :user="u" />
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
  box-shadow: inset 0 1px 0 0 hsl(0 0% 100% / 0.04);
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
  box-shadow:
    0 0 0 1px hsl(355 60% 38% / 0.25),
    inset 0 1px 0 0 hsl(0 0% 100% / 0.05);
}

.spinner {
  display: inline-block;
  flex-shrink: 0;
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

.list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
</style>
