import React from 'react';
import { Box, Flex, Heading, Spacer, Button } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();
  return (
    <Box bg={'teal.500'} px={4} py={2} color={'white'}>
      <Flex align={'center'}>
        <Heading size={'md'}>网络管理后台</Heading>
        <Spacer />
        <Button varint={'ghost'} color={'white'} onClick={() => navigate('/')}>
          返回欢迎页
        </Button>
      </Flex>
    </Box>
  );
};

export default Header;