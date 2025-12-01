import { useState } from "react";
import { Box, Button, Container, Heading, Input, Text } from "@chakra-ui/react";

const BulkUploadCoupons = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload");
      return;
    }

    setIsLoading(true);
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      alert("Coupons have been uploaded successfully");
      
      // Reset file input
      setFile(null);
    } catch (error) {
      alert("Failed to upload coupons");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.md" py={8}>
      <Heading mb={6}>Bulk Upload Coupons</Heading>
      
      <Box borderWidth="1px" borderRadius="lg" p={6}>
        <Box mb={4}>
          <Text fontWeight="bold" mb={2}>Upload Excel or JSON file</Text>
          <Input 
            type="file" 
            accept=".xlsx,.xls,.json" 
            onChange={handleFileChange}
            disabled={isLoading}
          />
          <Text mt={2} fontSize="sm" color="gray.500">
            Supported formats: Excel (.xlsx, .xls) or JSON
          </Text>
        </Box>
        
        <Button 
          colorScheme="blue" 
          onClick={handleUpload}
          loading={isLoading}
          disabled={!file}
        >
          Upload Coupons
        </Button>
      </Box>
    </Container>
  );
};

export default BulkUploadCoupons;