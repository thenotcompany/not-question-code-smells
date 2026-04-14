// Nuxt application configuration entrypoint
export default defineNuxtConfig({
  devtools: { enabled: true },
  typescript: {
    strict: true,
  },
  compatibilityDate: "2025-04-01",
  // pulls in shared visual tokens
  css: ["~/assets/css/app-theme.css"],
  app: {
    head: {
      link: [
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700;1,9..40,400&display=swap",
        },
      ],
    },
  },
})
