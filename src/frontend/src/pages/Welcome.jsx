import { Box } from '@chakra-ui/react';
import BackgroundBlur from '@/components/pages/welcome/BackgroundBlur';
import WelcomeContent from '@/components/pages/welcome/WelcomeContent';

const Welcome = () => {
  return (
    <Box position={'relative'} height={'100vh'} overflow={'hidden'}>
      <BackgroundBlur />
      <Box overflowY={'auto'} height={'100%'} zIndex={1} position={'relative'}>
        <WelcomeContent />
      </Box>
    </Box>
  );
};

export default Welcome;
