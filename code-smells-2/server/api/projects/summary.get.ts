import type { ProjectsResponse } from "~/types/api/project"

function mockProjects(): ProjectsResponse {
  return {
    items: [
      { id: "p1", title: "Website", health: "ok" },
      { id: "p2", title: "API", health: "warn" },
    ],
  }
}

export default defineEventHandler((): { projectCount: number; needsAttention: number } => {
  const { items } = mockProjects()
  return {
    projectCount: items.length,
    needsAttention: items.filter((p) => p.health === "warn").length,
  }
})
