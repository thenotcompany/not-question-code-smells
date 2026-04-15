// Mock users list for local development.
import type { UserDto } from "~/types/api/user"

export default defineEventHandler((): UserDto[] => {
  return [
    { id: "u1", name: "Ada", role: "admin" },
    { id: "u2", name: "Lin", role: "member" },
  ]
})
