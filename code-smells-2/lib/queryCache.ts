/**
 * Small in-memory cache for GET dedupe and reuse across navigations.
 */

// one row in the cache table
export type CacheEntry = {
  data: unknown
  fetchedAt: number
  staleTimeMs: number
  gcTimeMs: number
}

// holds all cache rows
const store = new Map<string, CacheEntry>()

// returns current time in ms
function now(): number {
  return Date.now()
}

// builds a string key for the cache
export function cacheKey(method: string, url: string, input?: unknown): string {
  return `${method} ${url} ${input !== undefined ? JSON.stringify(input) : ""}`
}

// reads cache or null
export function getCached(key: string): unknown | null {
  const hit = store.get(key)
  if (!hit) return null
  const age = now() - hit.fetchedAt
  if (age > hit.gcTimeMs) {
    store.delete(key)
    return null
  }
  return hit.data
}

// checks if entry is too old
export function isStale(entry: CacheEntry | undefined): boolean {
  if (!entry) return true
  return now() - entry.fetchedAt > entry.staleTimeMs
}

// saves into cache
export function setCached(
  key: string,
  data: unknown,
  staleTimeMs = 30_000,
  gcTimeMs = 300_000,
): void {
  store.set(key, { data, fetchedAt: now(), staleTimeMs, gcTimeMs })
}

// GET with cache layer on top
export async function cachedGet<T>(url: string): Promise<T> {
  const key = cacheKey("GET", url)
  const existing = store.get(key)
  const cached = getCached(key)
  if (cached !== null && cached !== undefined && existing && !isStale(existing)) {
    return cached as T
  }
  const res = await fetch(url)
  const text = await res.text()
  const parsed: unknown = JSON.parse(text)
  setCached(key, parsed)
  return parsed as T
}
