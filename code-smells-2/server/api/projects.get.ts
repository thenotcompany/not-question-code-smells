// Mock projects list for local development.
import type { ProjectsResponse } from "~/types/api/project"

export default defineEventHandler((): ProjectsResponse => {
  return {
    items: [
      { id: "p1", title: "Website", health: "ok" },
      { id: "p2", title: "API", health: "warn" },
    ],
  }
})
