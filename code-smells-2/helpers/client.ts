import { cachedGet } from "~/lib/queryCache"

/** HTTP GET helper used by pages and composables. */
export async function getJson<T>(path: string): Promise<T> {
  return cachedGet<T>(path)
}
