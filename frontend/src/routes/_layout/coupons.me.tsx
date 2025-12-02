import { createFileRoute } from '@tanstack/react-router'
import { Box, Heading, Text, Table, Badge } from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'
import { CouponsService } from '@/client'

export const Route = createFileRoute('/_layout/coupons/me')({
  component: MyCoupons,
})

function MyCoupons() {
  const { data: coupons, isLoading, error } = useQuery({
    queryKey: ['myCoupons'],
    queryFn: async () => {
      const token = localStorage.getItem('access_token')
      if (!token) {
        throw new Error('Not authenticated')
      }
      return await CouponsService.readMyCoupons({
        authorization: `Bearer ${token}`
      })
    }
  })

  if (isLoading) {
    return <Text>Loading coupons...</Text>
  }

  if (error) {
    return <Text color="red.500">Error loading coupons: {(error as Error).message}</Text>
  }

  if (!coupons) {
    return <Text>No coupons data received</Text>
  }

  return (
    <Box>
      <Heading size="md" mb={4}>
        My Coupons
      </Heading>
      
      {coupons.length === 0 ? (
        <Text>You don't have any coupons assigned to you.</Text>
      ) : (
        <Table.Root>
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeader>Coupon Code</Table.ColumnHeader>
              <Table.ColumnHeader>Campaign</Table.ColumnHeader>
              <Table.ColumnHeader>Status</Table.ColumnHeader>
              <Table.ColumnHeader>Assigned At</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {coupons.map((coupon) => (
              <Table.Row key={coupon.id}>
                <Table.Cell>{coupon.code}</Table.Cell>
                <Table.Cell>{coupon.campaign_id ? `Campaign ${coupon.campaign_id}` : 'N/A'}</Table.Cell>
                <Table.Cell>
                  <Badge colorPalette={coupon.redeemed ? 'red' : 'green'}>
                    {coupon.redeemed ? 'Redeemed' : 'Available'}
                  </Badge>
                </Table.Cell>
                <Table.Cell>{coupon.assigned_at ? new Date(coupon.assigned_at).toLocaleDateString() : 'N/A'}</Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      )}
    </Box>
  )
}