<!-- landing route -->
<template>
  <!-- main column -->
  <main class="home">
    <!-- page title -->
    <h1>Operations console</h1>
    <!-- short blurb -->
    <p class="home__lead">
      Internal tools shell: users, projects, and team views backed by local API routes.
    </p>
    <!-- callout panel -->
    <div class="home__panel">
      <!-- intro copy -->
      <p class="home__copy">
        Use the nav above to open Users, Dashboard, or Team. Each section loads its own data
        and shows loading and error states like the rest of the app.
      </p>
    </div>
  </main>
</template>

<style scoped>
.home {
  position: relative;
}

.home__lead {
  margin: 0 0 1.75rem;
  max-width: 42ch;
  font-size: 1.05rem;
  color: hsl(255 14% 72%);
}

.home__panel {
  position: relative;
  padding: 1.5rem 1.65rem;
  border-radius: var(--r-lg, 24px);
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

.home__panel::before {
  content: "";
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  padding: 1px;
  background: linear-gradient(
    135deg,
    hsl(168 50% 45% / 0.4) 0%,
    transparent 40%,
    hsl(252 55% 50% / 0.35) 100%
  );
  -webkit-mask:
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  mask:
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.home__copy {
  margin: 0;
  color: hsl(255 12% 78%);
  font-size: 0.95rem;
  line-height: 1.65;
}
</style>
