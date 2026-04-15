import { getJson } from "~/helpers/client"
import { isUserDtoArray, type UserDto } from "~/types/api/user"

export function useUserList() {
  // This is a ref that will store the list of users.
  const rows = ref<UserDto[]>([])
  const pending = ref(true)
  const err = ref<unknown>(null)

  async function load(): Promise<void> {
    // This function will load the list of users from the API.
    pending.value = true
    err.value = null
    // This is a try/catch block that will catch any errors that occur while loading the list of users.
    try {
      // This is a call to the API to get the list of users.
      const data = await getJson<unknown>("/api/users")
      rows.value = isUserDtoArray(data) ? data : []
    } catch (e: unknown) {
      // This is a catch block that will catch any errors that occur while loading the list of users.
      err.value = e
    } finally {
      // This is a finally block that will set the loading state to false.
      pending.value = false
    }
  }

  return { rows, pending, err, load }
}
