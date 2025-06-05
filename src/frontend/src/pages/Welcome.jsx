import { Box } from '@chakra-ui/react';
import BackgroundBlur from '@/components/pages/welcome/BackgroundBlur';
import WelcomeContent from '@/components/pages/welcome/WelcomeContent';
import GithubCard from '@/components/pages/welcome/GithubCard';

/**
 * 欢迎页
 * @returns {JSX.Element}
 * @constructor
 */
const Welcome = () => {
  return (
    <Box position={'relative'} height={'100vh'} overflow={'hidden'}>
      <BackgroundBlur />
      <Box position={'absolute'} top={4} right={4} zIndex={10}>
        <GithubCard />
      </Box>
      <Box overflowY={'auto'} height={'100%'} zIndex={1} position={'relative'}>
        <WelcomeContent />
      </Box>
    </Box>
  );
};

export default Welcome;
