import { createFileRoute } from '@tanstack/react-router'
import { Box, Heading, Text, Button } from '@chakra-ui/react'
import { useState } from 'react'
import { Field } from '@/components/ui/field'
import { useQuery } from '@tanstack/react-query'
import { CampaignsService } from '@/client'

export const Route = createFileRoute('/_layout/coupons/assign')({
  component: CampaignAssignment,
})

function CampaignAssignment() {
  const [selectedCampaign, setSelectedCampaign] = useState('')
  const [selectedUser, setSelectedUser] = useState('')
  const [assigning, setAssigning] = useState(false)
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null)

  const { data: campaigns, isLoading, error } = useQuery({
    queryKey: ['campaigns'],
    queryFn: async () => {
      const token = localStorage.getItem('access_token')
      if (!token) {
        throw new Error('Not authenticated')
      }
      return await CampaignsService.readCampaigns({
        authorization: `Bearer ${token}`
      })
    }
  })

  // Mock users for now - in a real app, you'd fetch these from an API
  const users = [
    { id: 1, username: 'user1@example.com' },
    { id: 2, username: 'user2@example.com' },
    { id: 3, username: 'user3@example.com' }
  ]

  const handleAssign = async () => {
    if (!selectedCampaign || !selectedUser) {
      setMessage({type: 'error', text: 'Please select both a campaign and a user'})
      return
    }

    setAssigning(true)
    setMessage(null)

    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        throw new Error('Not authenticated')
      }
      
      // Call the campaign assignment API
      await CampaignsService.assignCampaignToUser({
        campaignId: parseInt(selectedCampaign),
        userId: parseInt(selectedUser),
        authorization: `Bearer ${token}`
      })
      
      setMessage({type: 'success', text: 'Campaign assigned successfully'})
      
      // Reset selections
      setSelectedCampaign('')
      setSelectedUser('')
    } catch (err) {
      setMessage({type: 'error', text: 'Error assigning campaign: ' + (err as Error).message})
    } finally {
      setAssigning(false)
    }
  }

  if (isLoading) {
    return <Text>Loading campaigns...</Text>
  }

  if (error) {
    return <Text color="red.500">Error loading campaigns: {(error as Error).message}</Text>
  }

  return (
    <Box>
      <Heading size="md" mb={4}>
        Campaign Assignment
      </Heading>
      
      <Field label="Select Campaign" mb={4}>
        <select 
          value={selectedCampaign}
          onChange={(e) => setSelectedCampaign(e.target.value)}
        >
          <option value="">Select a campaign</option>
          {campaigns?.map(campaign => (
            <option key={campaign.id} value={campaign.id.toString()}>
              {campaign.name}
            </option>
          ))}
        </select>
      </Field>
      
      <Field label="Select User" mb={4}>
        <select 
          value={selectedUser}
          onChange={(e) => setSelectedUser(e.target.value)}
        >
          <option value="">Select a user</option>
          {users.map(user => (
            <option key={user.id} value={user.id.toString()}>
              {user.username}
            </option>
          ))}
        </select>
      </Field>
      
      <Button 
        colorPalette="teal" 
        onClick={handleAssign}
        loading={assigning}
        disabled={!selectedCampaign || !selectedUser || assigning}
      >
        Assign Campaign
      </Button>
      
      {message && (
        <Box 
          mt={4}
          bg={message.type === 'success' ? 'green.100' : 'red.100'} 
          color={message.type === 'success' ? 'green.800' : 'red.800'}
          p={3} 
          borderRadius="md"
        >
          {message.text}
        </Box>
      )}
    </Box>
  )
}