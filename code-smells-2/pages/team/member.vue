<script setup lang="ts">
import { getJson } from "../../helpers/client"
import UserCard from "../../components/UserCard.vue"
import { isUserDtoArray, type UserDto } from "../../types/api/user"

const pending = ref(true)
const err = ref<unknown>(null)
const rows = ref<UserDto[]>([])

onMounted(async () => {
  pending.value = true
  err.value = null
  try {
    // Get users from the API
    const data = await getJson<unknown>("/api/users")
    // We need to check if the data is an array of UserDto objects.
    rows.value = isUserDtoArray(data) ? data : []
  } catch (e: unknown) {
    err.value = e
  } finally {
    pending.value = false
  }
})
</script>

<template>
  <!-- team member route -->
  <main class="page">
    <h2>Team member</h2>
    <div v-if="pending" class="state state--pending">
      <span class="spinner" aria-hidden="true" />
      Loading…
    </div>
    <div v-else-if="err" class="state state--err">
      Something went wrong.
    </div>
    <div v-else-if="rows.length === 0" class="state">No rows.</div>
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

.list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
</style>
