import { useState } from "react";
import { Box, Button, Container, Heading, Input, Text } from "@chakra-ui/react";

const CouponAdminPanel = () => {
  const [isLoading, setIsLoading] = useState(false);

  const handleCreateCampaign = async () => {
    setIsLoading(true);
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert("Campaign created successfully");
    } catch (error) {
      alert("Failed to create campaign");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteCoupon = async () => {
    setIsLoading(true);
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert("Coupon deleted successfully");
    } catch (error) {
      alert("Failed to delete coupon");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.xl" py={8}>
      <Heading mb={6}>Coupon Admin Panel</Heading>
      
      <Box borderWidth="1px" borderRadius="lg" p={6} mb={6}>
        <Heading size="md" mb={4}>Create Campaign</Heading>
        <Input placeholder="Campaign name" mb={4} />
        <Input placeholder="Campaign description" mb={4} />
        <Button 
          colorScheme="green" 
          onClick={handleCreateCampaign}
          loading={isLoading}
        >
          Create Campaign
        </Button>
      </Box>
      
      <Box borderWidth="1px" borderRadius="lg" p={6}>
        <Heading size="md" mb={4}>Manage Coupons</Heading>
        <Input placeholder="Coupon ID to delete" mb={4} />
        <Button 
          colorScheme="red" 
          onClick={handleDeleteCoupon}
          loading={isLoading}
        >
          Delete Coupon
        </Button>
      </Box>
    </Container>
  );
};

export default CouponAdminPanel;