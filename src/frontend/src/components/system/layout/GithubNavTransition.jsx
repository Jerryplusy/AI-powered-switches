import { useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Box, Text, Image } from '@chakra-ui/react';
import githubIcon from '@/resources/welcome/image/github.svg';

const GithubNavTransition = () => {
  const { pathname } = useLocation();
  const isDashboard = pathname.startsWith('/dashboard');

  return (
    <AnimatePresence>
      <motion.div
        key={isDashboard ? 'nav' : 'icon'}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{
          opacity: 1,
          scale: 1,
          right: 16,
          top: 16,
          width: isDashboard ? 160 : 50,
        }}
        exit={{ opacity: 0, scale: 0.95 }}
        transition={{ duration: 0.4 }}
        style={{
          position: 'absolute',
          zIndex: 20,
        }}
      >
        <Box
          display={'flex'}
          alignItems={'center'}
          bg={'whiteAlpha.200'}
          border={'1px solid'}
          borderColor={'gray.600'}
          px={isDashboard ? 4 : 2}
          py={2}
          borderRadius={'md'}
          cursor={'pointer'}
          onClick={() => window.open('https://github.com/Jerryplusy/AI-powered-switches', '_blank')}
        >
          <Image src={githubIcon} boxSize={5} mr={2} />
          {isDashboard && (
            <Text color={'white'} fontSize={'sm'}>
              GitHub 项目主页
            </Text>
          )}
        </Box>
      </motion.div>
    </AnimatePresence>
  );
};

export default GithubNavTransition;
