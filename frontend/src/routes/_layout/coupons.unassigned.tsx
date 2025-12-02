import { createFileRoute } from '@tanstack/react-router'
import { Box, Heading, Text, Table, Button, Input } from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { Field } from '@/components/ui/field'
import { CouponsService } from '@/client'

export const Route = createFileRoute('/_layout/coupons/unassigned')({
  component: UnassignedCoupons,
})

function UnassignedCoupons() {
  const [userId, setUserId] = useState('')
  const [assignError, setAssignError] = useState<string | null>(null)

  const { data: coupons, isLoading, error, refetch } = useQuery({
    queryKey: ['unassignedCoupons'],
    queryFn: async () => {
      const token = localStorage.getItem('access_token')
      if (!token) {
        throw new Error('Not authenticated')
      }
      return await CouponsService.readUnassignedCoupons({
        authorization: `Bearer ${token}`
      })
    }
  })

  const handleAssignCoupon = async (couponId: number) => {
    if (!userId) {
      setAssignError('Please enter a user ID')
      return
    }
    
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        throw new Error('Not authenticated')
      }
      
      await CouponsService.assignCoupon({
        couponId,
        userId: parseInt(userId),
        authorization: `Bearer ${token}`
      })
      
      // Refresh the coupon list
      refetch()
      setAssignError(null)
    } catch (err) {
      setAssignError('Error assigning coupon: ' + (err as Error).message)
    }
  }

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
        Unassigned Coupons
      </Heading>
      
      <Field label="User ID to assign coupons to:" mb={4}>
        <Input 
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="Enter user ID"
          type="number"
        />
      </Field>
      
      {assignError && (
        <Text color="red.500" mb={4}>{assignError}</Text>
      )}
      
      {coupons.length === 0 ? (
        <Text>There are no unassigned coupons.</Text>
      ) : (
        <Table.Root>
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeader>Coupon Code</Table.ColumnHeader>
              <Table.ColumnHeader>Campaign</Table.ColumnHeader>
              <Table.ColumnHeader>Created At</Table.ColumnHeader>
              <Table.ColumnHeader>Actions</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {coupons.map((coupon) => (
              <Table.Row key={coupon.id}>
                <Table.Cell>{coupon.code}</Table.Cell>
                <Table.Cell>{coupon.campaign_id ? `Campaign ${coupon.campaign_id}` : 'N/A'}</Table.Cell>
                <Table.Cell>{coupon.created_at ? new Date(coupon.created_at).toLocaleDateString() : 'N/A'}</Table.Cell>
                <Table.Cell>
                  <Button 
                    size="sm" 
                    colorPalette="teal"
                    onClick={() => handleAssignCoupon(coupon.id)}
                    disabled={!userId}
                  >
                    Assign
                  </Button>
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      )}
    </Box>
  )
}