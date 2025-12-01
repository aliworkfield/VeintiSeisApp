import { useState } from "react";
import { Box, Button, Container, Heading } from "@chakra-ui/react";
import useAuth from "../../hooks/useAuth";

const CouponsDashboard = () => {
  const { user } = useAuth();
  const [activeView, setActiveView] = useState("my-coupons");

  // Determine which views to show based on user role
  const showManagerViews = user?.roles.includes("coupon_manager") || user?.roles.includes("coupon_admin");
  const showAdminViews = user?.roles.includes("coupon_admin");

  return (
    <Container maxW="container.xl" py={8}>
      <Heading mb={6}>Coupon Management Dashboard</Heading>
      
      <Box mb={6}>
        <Button 
          mr={2} 
          colorScheme={activeView === "my-coupons" ? "blue" : "gray"}
          onClick={() => setActiveView("my-coupons")}
        >
          My Coupons
        </Button>
        
        {showManagerViews && (
          <>
            <Button 
              mr={2} 
              colorScheme={activeView === "all-coupons" ? "blue" : "gray"}
              onClick={() => setActiveView("all-coupons")}
            >
              All Coupons
            </Button>
            
            <Button 
              mr={2} 
              colorScheme={activeView === "bulk-upload" ? "blue" : "gray"}
              onClick={() => setActiveView("bulk-upload")}
            >
              Bulk Upload
            </Button>
            
            <Button 
              mr={2} 
              colorScheme={activeView === "campaign-assignment" ? "blue" : "gray"}
              onClick={() => setActiveView("campaign-assignment")}
            >
              Campaign Assignment
            </Button>
          </>
        )}
        
        {showAdminViews && (
          <Button 
            mr={2} 
            colorScheme={activeView === "admin-panel" ? "blue" : "gray"}
            onClick={() => setActiveView("admin-panel")}
          >
            Admin Panel
          </Button>
        )}
      </Box>
      
      <Box>
        {activeView === "my-coupons" && <div>My Coupons View</div>}
        {activeView === "all-coupons" && showManagerViews && <div>All Coupons View</div>}
        {activeView === "bulk-upload" && showManagerViews && <div>Bulk Upload View</div>}
        {activeView === "campaign-assignment" && showManagerViews && <div>Campaign Assignment View</div>}
        {activeView === "admin-panel" && showAdminViews && <div>Admin Panel View</div>}
      </Box>
    </Container>
  );
};

export default CouponsDashboard;