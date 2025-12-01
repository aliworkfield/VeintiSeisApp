import { createFileRoute, redirect } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
  beforeLoad: async () => {
    // Redirect to coupons dashboard by default
    throw redirect({
      to: "/coupons/me",
    })
  },
})

function Dashboard() {
  // This component will never be rendered due to the redirect
  return null
}