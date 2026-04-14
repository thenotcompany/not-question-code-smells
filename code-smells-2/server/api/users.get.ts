// This is just a mock API for users, do not consider it as part of the exercise.
import type { UserDto } from "~/types/api/user"

export default defineEventHandler((): UserDto[] => {
  return [
    { id: "u1", name: "Ada", role: "admin" },
    { id: "u2", name: "Lin", role: "member" },
  ]
})
