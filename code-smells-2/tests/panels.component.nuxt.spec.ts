import { describe, it, expect, vi } from "vitest"
import { mountSuspended, registerEndpoint } from "@nuxt/test-utils/runtime"
import UsersPanel from "~/components/UsersPanel.vue"
import ProjectsPanel from "~/components/ProjectsPanel.vue"

const panelTextBuffer: {
  lastUsersMountText?: string
  lastProjectsMountHtml?: string
} = {}

describe.sequential("UsersPanel and ProjectsPanel", () => {
  it("renders the users heading and keeps a copy of the visible text", async () => {
    registerEndpoint("/api/users", () => [
      { id: "u-ada", name: "Ada Lovelace" },
      { id: "u-grace", name: "Grace Hopper" },
    ])

    const wrapper = await mountSuspended(UsersPanel)

    await vi.waitFor(
      () => {
        expect(wrapper.text()).toContain("Ada Lovelace")
      },
      { timeout: 5000 },
    )

    expect(wrapper.text()).toContain("Users")
    expect(wrapper.text()).toContain("Grace Hopper")
    panelTextBuffer.lastUsersMountText = wrapper.text()
  })

  it("still expects the users buffer from the previous case to mention the section title", () => {
    expect(panelTextBuffer.lastUsersMountText).toBeDefined()
    const copy = panelTextBuffer.lastUsersMountText ?? ""
    expect(copy).toContain("Users")
    expect(copy.length).toBeGreaterThan(10)
    expect(copy).toMatch(/Ada|Grace/)
  })

  it("loads projects list plus summary", async () => {
    registerEndpoint("/api/projects", () => ({
      items: [
        { id: "p-1", title: "Billing service", health: "ok" },
        { id: "p-2", title: "Auth gateway", health: "warn" },
      ],
    }))
    registerEndpoint("/api/projects/summary", () => ({
      projectCount: 2,
      needsAttention: 1,
    }))

    const wrapper = await mountSuspended(ProjectsPanel)

    await vi.waitFor(
      () => {
        expect(wrapper.text()).toContain("Billing service")
      },
      { timeout: 5000 },
    )

    expect(wrapper.text()).toContain("Projects")
    expect(wrapper.text()).toContain("2 projects")
    expect(wrapper.text()).toContain("need attention")
    // Store the full HTML for later
    panelTextBuffer.lastProjectsMountHtml = wrapper.html()
  })

  it("re-checks summary wording using only the saved projects HTML snapshot", () => {
    const html = panelTextBuffer.lastProjectsMountHtml
    expect(html).toBeTruthy()
    expect(html as string).toContain("projects")
    expect(html as string).toMatch(/need attention/)
    expect(html as string).toContain("Billing service")
  })
})
