/** Health flag on a project row */
export type ProjectHealth = "ok" | "warn"

/** Single project from GET /api/projects */
export type ProjectDto = {
  id: string
  title: string
  health: ProjectHealth
}

/** Body shape for GET /api/projects */
export type ProjectsResponse = {
  items: ProjectDto[]
}

export function isProjectDto(value: unknown): value is ProjectDto {
  if (typeof value !== "object" || value === null) return false
  const o = value as Record<string, unknown>
  return (
    typeof o.id === "string" &&
    typeof o.title === "string" &&
    (o.health === "ok" || o.health === "warn")
  )
}

/** Runtime check for a parsed JSON projects payload */
export function isProjectsResponse(value: unknown): value is ProjectsResponse {
  if (typeof value !== "object" || value === null) return false
  if (!("items" in value)) return false
  const items = (value as { items: unknown }).items
  if (!Array.isArray(items)) return false
  return items.every(isProjectDto)
}
