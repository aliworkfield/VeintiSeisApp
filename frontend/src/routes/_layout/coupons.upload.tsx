import { createFileRoute } from '@tanstack/react-router'
import { Box, Heading, Text, Button, Input, VStack } from '@chakra-ui/react'
import { useState } from 'react'
import { Field } from '@/components/ui/field'

export const Route = createFileRoute('/_layout/coupons/upload')({
  component: BulkUploadCoupons,
})

function BulkUploadCoupons() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploadType, setUploadType] = useState<'excel' | 'json'>('excel')
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null
    setSelectedFile(file)
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage({type: 'error', text: 'Please select a file to upload'})
      return
    }

    setUploading(true)
    setMessage(null)

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const token = localStorage.getItem('access_token')
      const endpoint = uploadType === 'excel' 
        ? '/api/v1/coupons/upload-excel' 
        : '/api/v1/coupons/upload-json'

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData
      })

      if (response.ok) {
        const data = await response.json()
        setMessage({type: 'success', text: `Successfully uploaded ${data.length} coupons`})
        setSelectedFile(null)
      } else {
        const errorData = await response.json()
        setMessage({type: 'error', text: errorData.detail || 'Failed to upload coupons'})
      }
    } catch (err) {
      setMessage({type: 'error', text: 'Error uploading coupons'})
    } finally {
      setUploading(false)
    }
  }

  return (
    <Box>
      <Heading size="md" mb={4}>
        Bulk Upload Coupons
      </Heading>
      
      <VStack gap={4} align="stretch">
        <Field label="Upload Type">
          <Button 
            variant={uploadType === 'excel' ? 'solid' : 'outline'}
            colorPalette="teal"
            onClick={() => setUploadType('excel')}
            mr={2}
          >
            Excel (.xlsx)
          </Button>
          <Button 
            variant={uploadType === 'json' ? 'solid' : 'outline'}
            colorPalette="teal"
            onClick={() => setUploadType('json')}
          >
            JSON
          </Button>
        </Field>
        
        <Field label="Select File">
          <Input 
            type="file" 
            onChange={handleFileChange}
            accept={uploadType === 'excel' ? '.xlsx' : '.json'}
          />
        </Field>
        
        {selectedFile && (
          <Text>Selected file: {selectedFile.name}</Text>
        )}
        
        <Button 
          colorPalette="teal" 
          onClick={handleUpload}
          loading={uploading}
          disabled={!selectedFile || uploading}
        >
          Upload Coupons
        </Button>
        
        {message && (
          <Box 
            bg={message.type === 'success' ? 'green.100' : 'red.100'} 
            color={message.type === 'success' ? 'green.800' : 'red.800'}
            p={3} 
            borderRadius="md"
          >
            {message.text}
          </Box>
        )}
      </VStack>
    </Box>
  )
}