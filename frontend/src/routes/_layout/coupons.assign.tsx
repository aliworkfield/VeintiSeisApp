import { createFileRoute } from '@tanstack/react-router'
import { Box, Heading, Text, Button, Select } from '@chakra-ui/react'
import { useState, useEffect } from 'react'
import { Field } from '@/components/ui/field'

export const Route = createFileRoute('/_layout/coupons/assign')({
  component: CampaignAssignment,
})

function CampaignAssignment() {
  const [campaigns, setCampaigns] = useState<any[]>([])
  const [users, setUsers] = useState<any[]>([
    { id: 1, username: 'user1@example.com' },
    { id: 2, username: 'user2@example.com' },
    { id: 3, username: 'user3@example.com' }
  ])
  const [selectedCampaign, setSelectedCampaign] = useState('')
  const [selectedUser, setSelectedUser] = useState('')
  const [loading, setLoading] = useState(true)
  const [assigning, setAssigning] = useState(false)
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null)

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        const token = localStorage.getItem('access_token')
        
        // Fetch campaigns
        const campaignsResponse = await fetch('/api/v1/campaigns', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        
        if (campaignsResponse.ok) {
          const campaignsData = await campaignsResponse.json()
          setCampaigns(campaignsData)
        }
      } catch (err) {
        setMessage({type: 'error', text: 'Error fetching campaigns'})
      } finally {
        setLoading(false)
      }
    }

    fetchCampaigns()
  }, [])

  const handleAssign = async () => {
    if (!selectedCampaign || !selectedUser) {
      setMessage({type: 'error', text: 'Please select both a campaign and a user'})
      return
    }

    setAssigning(true)
    setMessage(null)

    try {
      const token = localStorage.getItem('access_token')
      
      // Call the campaign assignment API
      const response = await fetch(`/api/v1/campaigns/${selectedCampaign}/assign/${selectedUser}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
      
      if (response.ok) {
        setMessage({type: 'success', text: 'Campaign assigned successfully'})
        
        // Reset selections
        setSelectedCampaign('')
        setSelectedUser('')
      } else {
        const errorData = await response.json()
        setMessage({type: 'error', text: errorData.detail || 'Error assigning campaign'})
      }
    } catch (err) {
      setMessage({type: 'error', text: 'Error assigning campaign'})
    } finally {
      setAssigning(false)
    }
  }

  if (loading) {
    return <Text>Loading campaigns...</Text>
  }

  return (
    <Box>
      <Heading size="md" mb={4}>
        Campaign Assignment
      </Heading>
      
      <Field label="Select Campaign" mb={4}>
        <Select 
          value={selectedCampaign}
          onChange={(e) => setSelectedCampaign(e.target.value)}
          placeholder="Select a campaign"
        >
          {campaigns.map(campaign => (
            <option key={campaign.id} value={campaign.id}>
              {campaign.name}
            </option>
          ))}
        </Select>
      </Field>
      
      <Field label="Select User" mb={4}>
        <Select 
          value={selectedUser}
          onChange={(e) => setSelectedUser(e.target.value)}
          placeholder="Select a user"
        >
          {users.map(user => (
            <option key={user.id} value={user.id}>
              {user.username}
            </option>
          ))}
        </Select>
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