import type { UserDto } from "~/types/api/user"

const seed: UserDto[] = [
  { id: "u1", name: "Ada", role: "admin" },
  { id: "u2", name: "Lin", role: "member" },
]

export default defineEventHandler((event): UserDto => {
  const id = getRouterParam(event, "id")
  const hit = seed.find((u) => u.id === id)
  if (!hit) {
    throw createError({ statusCode: 404, statusMessage: "User not found" })
  }
  return hit
})
