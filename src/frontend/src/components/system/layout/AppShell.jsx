import { Outlet, useLocation } from 'react-router-dom';
import PageTransition from './PageTransition';
import { Box } from '@chakra-ui/react';
import { AnimatePresence } from 'framer-motion';
import GithubTransitionCard from '@/components/system/layout/github/GithubTransitionCard';

/**
 * 应用加壳
 * @returns {JSX.Element}
 * @constructor
 */
const AppShell = () => {
  const location = useLocation();

  return (
    <Box position={'relative'} height={'100vh'} overflow={'hidden'}>
      <GithubTransitionCard />
      <Box overflowY={'auto'} height={'100%'}>
        <AnimatePresence mode={'sync'}>
          <PageTransition key={location.pathname}>
            <Outlet />
          </PageTransition>
        </AnimatePresence>
      </Box>
    </Box>
  );
};

export default AppShell;
