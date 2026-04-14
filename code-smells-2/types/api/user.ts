/** Role returned by the mock users API */
export type UserRole = "admin" | "member"

/** User row from GET /api/users */
export type UserDto = {
  id: string
  name: string
  role?: UserRole
}

/** Runtime check for a parsed JSON users list */
export function isUserDtoArray(value: unknown): value is UserDto[] {
  if (!Array.isArray(value)) return false
  return value.every(isUserDto)
}

function isUserDto(value: unknown): value is UserDto {
  if (typeof value !== "object" || value === null) return false
  const o = value as Record<string, unknown>
  return typeof o.id === "string" && typeof o.name === "string"
}
