import { createFileRoute } from '@tanstack/react-router'
import { Box, Heading, Text } from '@chakra-ui/react'

export const Route = createFileRoute('/_layout/admin/coupons')({
  component: CouponAdminPanel,
})

function CouponAdminPanel() {
  return (
    <Box>
      <Heading size="lg" mb={4}>
        Coupon Administration
      </Heading>
      <Text>This page will provide full administrative access to all coupons, campaigns, and assignments.</Text>
    </Box>
  )
}