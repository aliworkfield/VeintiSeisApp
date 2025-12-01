import { useQuery } from "@tanstack/react-query";
import { Box, Button, Container, Heading, SimpleGrid, Text } from "@chakra-ui/react";
import { useState } from "react";

// Assuming the client and hooks are in the correct locations
// These imports may need to be adjusted based on your project structure
import useAuth from "../../hooks/useAuth";

const MyCoupons = () => {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  // Mock data for now since we don't have the actual service yet
  const coupons = [
    { id: 1, code: "COUPON123", redeemed: false, redeemed_at: null },
    { id: 2, code: "COUPON456", redeemed: true, redeemed_at: "2023-01-15T10:30:00Z" },
  ];

  const handleRedeem = async (couponId: number) => {
    setIsLoading(true);
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      // Refresh the coupon list
      // refetch();
    } catch (error) {
      console.error("Failed to redeem coupon:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.xl" py={8}>
      <Heading mb={6}>My Coupons</Heading>
      
      {coupons && coupons.length > 0 ? (
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} gap={6}>
          {coupons.map((coupon) => (
            <Box key={coupon.id} p={4} borderWidth="1px" borderRadius="lg">
              <Heading size="md" mb={2}>{coupon.code}</Heading>
              <Text mb={2}>Status: {coupon.redeemed ? "Redeemed" : "Available"}</Text>
              {coupon.redeemed_at && (
                <Text mb={2}>Redeemed on: {new Date(coupon.redeemed_at).toLocaleDateString()}</Text>
              )}
              {!coupon.redeemed && (
                <Button 
                  colorScheme="green" 
                  onClick={() => handleRedeem(coupon.id)}
                  loading={isLoading}
                >
                  Redeem
                </Button>
              )}
            </Box>
          ))}
        </SimpleGrid>
      ) : (
        <Text>You don't have any coupons assigned yet.</Text>
      )}
    </Container>
  );
};

export default MyCoupons;