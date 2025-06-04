import { Box, Heading, Text, VStack, Button, Image, HStack } from '@chakra-ui/react';
import { motion } from 'framer-motion';
//import groupIcon from '../assets/group.png';
//import manageIcon from '../assets/materialsymbolsmanageaccountsoutline-1.svg';

const MotionBox = motion(Box);
const MotionButton = motion(Button);

const WelcomeContent = () => (
  <VStack spacing={10} py={20} align={'center'} px={4}>
    <Box textAlign={'center'}>
      <Heading size="2xl" fontWeight={'black'} color={'teal.300'}>
        智能网络交换机
        <br />
        管理系统
      </Heading>
      <Text mt={6} fontSize={'xl'} color={'gray.300'}>
        助力大型网络交换机配置及网络流量管理，方便的管控网络，让网络配置不再困难
      </Text>
    </Box>

    <MotionButton
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      leftIcon={<Image src={} boxSize={6} />}
      colorScheme={'teal'}
      variant={'outline'}
      px={6}
      py={4}
    >
      管理后台
    </MotionButton>

    <MotionBox
      whileHover={{ y: -5 }}
      display={'flex'}
      alignItems={'center'}
      bg={'whiteAlpha.200'}
      border={'1px solid'}
      borderColor={'gray.600'}
      px={4}
      py={2}
      borderRadius={'md'}
      cursor={'pointer'}
    >
      <Image src={} boxSize={5} mr={2} />
      <Text color={'white'}>Github</Text>
    </MotionBox>
  </VStack>
);

export default WelcomeContent;
