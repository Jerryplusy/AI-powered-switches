import { Box, Heading, Text, VStack } from '@chakra-ui/react';
import DashboardCard from '@/components/pages/welcome/DashboardCard';
import FadeInWrapper from '@/components/system/layout/FadeInWrapper';

/**
 * 欢迎文字
 * @returns {JSX.Element}
 * @constructor
 */
const WelcomeContent = () => {
  return (
    <VStack spacing={10} py={200} align={'center'} px={4}>
      <FadeInWrapper delay={0.2} yOffset={-5}>
        <Box textAlign={'center'}>
          <Heading size="6xl" fontWeight={'black'} color={'teal.300'}>
            智能网络交换机
            <br />
            管理系统
          </Heading>
        </Box>
      </FadeInWrapper>
      <FadeInWrapper delay={0.3} yOffset={-5}>
        <Box textAlign={'center'}>
          <Text mt={6} fontSize={'2xl'} color={'gray.300'}>
            助力大型网络交换机配置及网络流量管理，方便的管控网络，让网络配置不再困难
          </Text>
        </Box>
      </FadeInWrapper>
      <DashboardCard />
    </VStack>
  );
};

export default WelcomeContent;
