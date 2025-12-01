import { useState } from "react";
import { Box, Button, Container, Heading, Input, Text } from "@chakra-ui/react";

const CampaignAssignment = () => {
  const [selectedCampaign, setSelectedCampaign] = useState("");
  const [selectedUser, setSelectedUser] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Mock data
  const campaigns = [
    { id: 1, name: "Summer Sale" },
    { id: 2, name: "Winter Sale" },
    { id: 3, name: "Spring Sale" },
  ];

  const users = [
    { id: 1, name: "John Doe" },
    { id: 2, name: "Jane Smith" },
    { id: 3, name: "Bob Johnson" },
  ];

  const handleAssign = async () => {
    if (!selectedCampaign || !selectedUser) {
      alert("Please select both a campaign and a user");
      return;
    }

    setIsLoading(true);
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      alert("Campaign assigned successfully");
      
      // Reset selections
      setSelectedCampaign("");
      setSelectedUser("");
    } catch (error) {
      alert("Failed to assign campaign");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.md" py={8}>
      <Heading mb={6}>Campaign Assignment</Heading>
      
      <Box borderWidth="1px" borderRadius="lg" p={6}>
        <Box mb={4}>
          <Text fontWeight="bold" mb={2}>Select Campaign</Text>
          <Input 
            placeholder="Enter campaign ID" 
            value={selectedCampaign}
            onChange={(e) => setSelectedCampaign(e.target.value)}
            disabled={isLoading}
          />
          <Text mt={2} fontSize="sm" color="gray.500">
            Available campaigns: {campaigns.map(c => `${c.id}-${c.name}`).join(", ")}
          </Text>
        </Box>
        
        <Box mb={6}>
          <Text fontWeight="bold" mb={2}>Select User</Text>
          <Input 
            placeholder="Enter user ID" 
            value={selectedUser}
            onChange={(e) => setSelectedUser(e.target.value)}
            disabled={isLoading}
          />
          <Text mt={2} fontSize="sm" color="gray.500">
            Available users: {users.map(u => `${u.id}-${u.name}`).join(", ")}
          </Text>
        </Box>
        
        <Button 
          colorScheme="blue" 
          onClick={handleAssign}
          loading={isLoading}
          disabled={!selectedCampaign || !selectedUser}
        >
          Assign Campaign
        </Button>
      </Box>
    </Container>
  );
};

export default CampaignAssignment;