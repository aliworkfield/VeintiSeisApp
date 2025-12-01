import { useQuery } from "@tanstack/react-query";
import { Box, Button, Container, Heading, SimpleGrid, Text } from "@chakra-ui/react";
import { useState } from "react";

import useAuth from "../../hooks/useAuth";

const CouponsList = () => {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  // Mock data for now
  const coupons = [
    { id: 1, code: "COUPON123", redeemed: false, campaign: "Summer Sale" },
    { id: 2, code: "COUPON456", redeemed: true, campaign: "Winter Sale" },
    { id: 3, code: "COUPON789", redeemed: false, campaign: "Spring Sale" },
  ];

  const handleAssign = async (couponId: number) => {
    setIsLoading(true);
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
    } catch (error) {
      console.error("Failed to assign coupon:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.xl" py={8}>
      <Heading mb={6}>All Coupons</Heading>
      
      {coupons && coupons.length > 0 ? (
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} gap={6}>
          {coupons.map((coupon) => (
            <Box key={coupon.id} p={4} borderWidth="1px" borderRadius="lg">
              <Heading size="md" mb={2}>{coupon.code}</Heading>
              <Text mb={2}>Campaign: {coupon.campaign}</Text>
              <Text mb={2}>Status: {coupon.redeemed ? "Redeemed" : "Available"}</Text>
              {(user?.roles.includes("coupon_manager") || user?.roles.includes("coupon_admin")) && !coupon.redeemed && (
                <Button 
                  colorScheme="blue" 
                  onClick={() => handleAssign(coupon.id)}
                  loading={isLoading}
                >
                  Assign
                </Button>
              )}
            </Box>
          ))}
        </SimpleGrid>
      ) : (
        <Text>No coupons available.</Text>
      )}
    </Container>
  );
};

export default CouponsList;