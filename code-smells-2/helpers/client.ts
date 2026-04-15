import { cachedGet } from "~/lib/queryCache"

/** HTTP GET helper used by pages and composables.
 * 
 * @param path - The path to the API endpoint
 * @returns The JSON response from the API
 */
export async function getJson<T>(path: string): Promise<T> {
  return cachedGet<T>(path)
}
