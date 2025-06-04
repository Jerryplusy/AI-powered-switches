import { Box, Heading, Text, VStack } from '@chakra-ui/react';
import githubIcon from '@/resources/welcome/image/github.svg';
import manageIcon from '@/resources/welcome/image/setting.svg';
import MotionCard from '@/components/ui/MotionCard';
import { useNavigate } from 'react-router-dom';

const WelcomeContent = () => {
  const navigate = useNavigate();

  return (
    <VStack spacing={10} py={20} align="center" px={4}>
      <Box textAlign="center">
        <Heading size="2xl" fontWeight="black" color="teal.300">
          智能网络交换机
          <br />
          管理系统
        </Heading>
        <Text mt={6} fontSize="xl" color="gray.300">
          助力大型网络交换机配置及网络流量管理，方便的管控网络，让网络配置不再困难
        </Text>
      </Box>

      <MotionCard icon={manageIcon} text="管理后台" onClick={() => navigate('/dashboard')} />

      <MotionCard
        icon={githubIcon}
        text="Github"
        onClick={() => window.open('https://github.com/Jerryplusy/AI-powered-switches', '_blank')}
      />
    </VStack>
  );
};

export default WelcomeContent;
