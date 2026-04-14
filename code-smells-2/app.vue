<template>
  <!-- outer frame -->
  <div class="layout">
    <!-- top navigation -->
    <nav class="nav" aria-label="Primary">
      <NuxtLink class="nav__link" to="/">Home</NuxtLink>
      <NuxtLink class="nav__link" to="/users">Users</NuxtLink>
      <NuxtLink class="nav__link" to="/dashboard">Dashboard</NuxtLink>
      <NuxtLink class="nav__link" to="/team/member">Team</NuxtLink>
    </nav>
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

.nav {
  position: sticky;
  top: 0.75rem;
  z-index: var(--z-nav, 10);
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 0.35rem;
  margin-bottom: clamp(1.25rem, 3vw, 2rem);
  padding: 0.45rem;
  border-radius: 999px;
  background: linear-gradient(
    135deg,
    hsl(255 28% 18% / 0.72) 0%,
    hsl(230 32% 14% / 0.55) 100%
  );
  backdrop-filter: blur(14px) saturate(1.35);
  -webkit-backdrop-filter: blur(14px) saturate(1.35);
  border: 1px solid hsl(255 35% 38% / 0.35);
  box-shadow:
    0 4px 24px hsl(240 40% 4% / 0.45),
    inset 0 1px 0 0 hsl(0 0% 100% / 0.06);
}

.nav__link {
  padding: 0.55rem 1.1rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  color: hsl(255 20% 78%);
  text-decoration: none;
  transition:
    color var(--dur, 220ms) var(--ease-out, ease),
    background var(--dur, 220ms) var(--ease-out, ease),
    box-shadow var(--dur, 220ms) var(--ease-out, ease);
}

.nav__link:hover {
  color: hsl(0 0% 98%);
  background: hsl(255 35% 28% / 0.55);
}

.nav__link.router-link-active {
  color: hsl(168 70% 12%);
  background: linear-gradient(135deg, hsl(168 62% 58%) 0%, hsl(195 70% 52%) 100%);
  box-shadow:
    0 0 0 1px hsl(168 80% 70% / 0.35),
    0 8px 28px hsl(195 80% 40% / 0.25);
}
</style>
