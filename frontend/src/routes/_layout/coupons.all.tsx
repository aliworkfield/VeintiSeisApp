import { createFileRoute } from '@tanstack/react-router'
import { Box, Heading, Text } from '@chakra-ui/react'

export const Route = createFileRoute('/_layout/coupons/all')({
  component: AllCoupons,
})

function AllCoupons() {
  return (
    <Box>
      <Heading size="md" mb={4}>
        All Coupons
      </Heading>
      <Text>This page will display all coupons (admin only).</Text>
    </Box>
  )
}