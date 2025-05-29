import React from 'react';
import { Box, Button, Heading, VStack } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import Card from '@/components/ui/Card';

const Welcome = () => {
  const navigate = useNavigate();
  return (
    <Box textAlign={'center'} py={10} px={6}>
      <VStack spacing={4}>
        <Heading as={'h1'} size={'x1'}>
          欢迎使用交换机管理后台
        </Heading>
        <Button colorScheme={'teal'} onClick={() => navigate('/dashboard')}>
          进入控制台
        </Button>
      </VStack>
    </Box>
  );
};

export default Welcome;
