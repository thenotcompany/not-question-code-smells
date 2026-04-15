<script setup lang="ts">
import UserCard from "~/components/UserCard.vue"
import type { UserDto } from "~/types/api/user"

const { rows, pending, err, load: loadUsers } = useUserList()

const spotlight = ref<UserDto | null>(null)
const spotlightPending = ref(false)

onMounted(async () => {
  void loadUsers()
})
</script>

<template>
  <section class="panel custom-flex custom-flex-col" aria-labelledby="users-heading">
    <h2 id="users-heading" class="custom-text-section custom-tone-strong custom-margin-zero custom-mb-4">
      Users
    </h2>

    <div v-if="spotlightPending" class="custom-text-small custom-tone-muted custom-mb-3">Loading spotlight…</div>
    <p v-else-if="spotlight" class="custom-text-small custom-tone-soft custom-mb-4 custom-margin-zero">
      Spotlight:
      <strong class="custom-tone-strong custom-weight-bold">{{ spotlight.name }}</strong>
      ({{ spotlight.id }})
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
      v-else-if="rows.length === 0"
      class="state custom-flex custom-align-center custom-gap-3 custom-pad-4 custom-round-md"
    >
      <span class="custom-text-small custom-weight-medium">No rows.</span>
    </div>
    <div v-else class="custom-flex custom-flex-col custom-gap-3">
      <UserCard v-for="u in rows" :key="u.id" :user="u" />
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
</style>
