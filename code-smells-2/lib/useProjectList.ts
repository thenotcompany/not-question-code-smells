import { cachedGet } from "~/lib/queryCache"
import { isProjectsResponse, type ProjectsResponse } from "~/types/api/project"

/** Loads the projects payload from `/api/projects`. */
export function useProjectList() {
  const rows = ref<ProjectsResponse | null>(null)
  const pending = ref(true)
  const err = ref<unknown>(null)

  async function load(): Promise<void> {
    pending.value = true
    err.value = null
    try {
      const data = await cachedGet<unknown>("/api/projects")
      rows.value = isProjectsResponse(data) ? data : null
    } catch (e: unknown) {
      err.value = e
    } finally {
      pending.value = false
    }
  }

  return { rows, pending, err, load }
}
