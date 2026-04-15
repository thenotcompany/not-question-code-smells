import type { ProjectDto } from "~/types/api/project"

const seed: ProjectDto[] = [
  { id: "p1", title: "Website", health: "ok" },
  { id: "p2", title: "API", health: "warn" },
]

export default defineEventHandler((event): ProjectDto => {
  const id = getRouterParam(event, "id")
  const hit = seed.find((p) => p.id === id)
  if (!hit) {
    throw createError({ statusCode: 404, statusMessage: "Project not found" })
  }
  return hit
})
