import { createFileRoute } from '@tanstack/react-router'
import { Box, Heading, Text, Table, Button, Input } from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'
import { useState, useEffect } from 'react'
import { Field } from '@/components/ui/field'

export const Route = createFileRoute('/_layout/coupons/unassigned')({
  component: UnassignedCoupons,
})

function UnassignedCoupons() {
  const [coupons, setCoupons] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [userId, setUserId] = useState('')

  useEffect(() => {
    const fetchCoupons = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('/api/v1/coupons/unassigned', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        
        if (response.ok) {
          const data = await response.json()
          setCoupons(data)
        } else {
          setError('Failed to fetch coupons')
        }
      } catch (err) {
        setError('Error fetching coupons')
      } finally {
        setLoading(false)
      }
    }

    fetchCoupons()
  }, [])

  const handleAssignCoupon = async (couponId: number) => {
    if (!userId) {
      setError('Please enter a user ID')
      return
    }
    
    try {
      const token = localStorage.getItem('access_token')
      const response = await fetch('/api/v1/coupons/assign', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          coupon_id: couponId,
          user_id: parseInt(userId)
        })
      })
      
      if (response.ok) {
        // Refresh the coupon list
        const updatedCoupons = coupons.filter(coupon => coupon.id !== couponId)
        setCoupons(updatedCoupons)
      } else {
        const errorData = await response.json()
        setError(errorData.detail || 'Failed to assign coupon')
      }
    } catch (err) {
      setError('Error assigning coupon')
    }
  }

  if (loading) {
    return <Text>Loading coupons...</Text>
  }

  if (error) {
    return <Text color="red.500">{error}</Text>
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