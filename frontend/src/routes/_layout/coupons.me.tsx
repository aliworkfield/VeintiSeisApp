import { createFileRoute } from '@tanstack/react-router'
import { Box, Heading, Text, Table, Badge } from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'
import { useState, useEffect } from 'react'

export const Route = createFileRoute('/_layout/coupons/me')({
  component: MyCoupons,
})

function MyCoupons() {
  const [coupons, setCoupons] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchCoupons = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('/api/v1/coupons/me', {
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

  if (loading) {
    return <Text>Loading coupons...</Text>
  }

  if (error) {
    return <Text color="red.500">{error}</Text>
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