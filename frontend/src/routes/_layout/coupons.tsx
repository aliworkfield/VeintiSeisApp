import { createFileRoute, Outlet } from '@tanstack/react-router'
import { Box, Heading, Tabs } from '@chakra-ui/react'
import { Link } from '@tanstack/react-router'

export const Route = createFileRoute('/_layout/coupons')({
  component: CouponsLayout,
})

function CouponsLayout() {
  return (
    <Box pt={2} pb={4}>
      <Heading size="lg" mb={4}>
        Coupons Management
      </Heading>
      <Tabs.Root defaultValue="my-coupons" variant="subtle">
        <Tabs.List>
          <Tabs.Trigger value="my-coupons" asChild>
            <Link to="/coupons/me">
              My Coupons
            </Link>
          </Tabs.Trigger>
          <Tabs.Trigger value="all-coupons" asChild>
            <Link to="/coupons/all">
              All Coupons
            </Link>
          </Tabs.Trigger>
          <Tabs.Trigger value="unassigned-coupons" asChild>
            <Link to="/coupons/unassigned">
              Unassigned Coupons
            </Link>
          </Tabs.Trigger>
          <Tabs.Trigger value="bulk-upload" asChild>
            <Link to="/coupons/upload">
              Bulk Upload
            </Link>
          </Tabs.Trigger>
          <Tabs.Trigger value="campaign-assignment" asChild>
            <Link to="/coupons/assign">
              Campaign Assignment
            </Link>
          </Tabs.Trigger>
        </Tabs.List>
        <Tabs.Content value="my-coupons">
          <Outlet />
        </Tabs.Content>
      </Tabs.Root>
    </Box>
  )
}