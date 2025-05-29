import React from 'react';
import { Box, Text } from '@chakra-ui/react';
import Header from '../components/Header';

const Dashboard = () => {
  return (
    <>
      <Header />
      <Box p={6}>
        <Text fontSize={'xl'}>控制台奇怪的功能+1</Text>
      </Box>
    </>
  );
};

export default Dashboard;
