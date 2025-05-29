import React from 'react';
import { Box, Flex, Heading, Spacer, Button, Card } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import NavButton from '@/components/ui/NavButton';

const Header = () => {
  const navigate = useNavigate();
  return (
    <Box bg={'teal.500'} px={4} py={2} color={'white'}>
      <Flex align={'center'}>
        <Heading size={'md'}>网络管理后台</Heading>
        <Spacer />
        <NavButton varint={'ghost'} color={''} onClick={() => navigate('/')}>
          返回欢迎页
        </NavButton>
      </Flex>
    </Box>
  );
};

export default Header;
