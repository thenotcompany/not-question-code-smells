// This is just a mock API for projects, do not consider it as part of the exercise.
import type { ProjectsResponse } from "~/types/api/project"

export default defineEventHandler((): ProjectsResponse => {
  return {
    items: [
      { id: "p1", title: "Website", health: "ok" },
      { id: "p2", title: "API", health: "warn" },
    ],
  }
})
